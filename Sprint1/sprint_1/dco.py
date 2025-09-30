# Import necessary modules
from io import BytesIO  # Import BytesIO for handling binary data
from PIL import Image  # Use PIL instead of tkinter for image handling
import requests  # Import requests for making HTTP requests
from urllib.parse import urlencode  # Import urlencode for URL encoding

class Datacube:
    def _init_(self, dbc):
        # """Initialize Datacube object."""
        self.dbc = dbc  # Store the provided DatabaseConnection object
        self.operations = []  # Initialize an empty list to store operations

    def add_operation(self, operation):
        """Add operation to the list of operations."""
        self.operations.append(operation)  # Append the provided operation to the list of operations

    def generate_query(self):
        """Generate WCPS query based on added operations."""
        if not self.operations:
            raise ValueError("No operations added. Please add operations before generating a query.")
        
        # Extract unique coverage names from operations
        unique_operations = set(op[0] for op in self.operations)
        # Construct WCPS query
        wcps_query = f"for $c in ({', '.join(unique_operations)})\nreturn\n"
        wcps_query += " ".join(self.to_wcps(op) for op in self.operations)
        return wcps_query

    def execute_query(self, wcps_query):
        """Execute WCPS query and return response."""
        try:
            response = requests.post(self.dbc.url, data={'query': wcps_query}, verify=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.content.decode()  # Decode the response content and return it
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error executing WCPS query: {e}")  # Raise a connection error if request fails

    def subset(self, coverage, time, E1, E2, N1, N2):
        """Perform subset operation."""
        operation = (coverage, time, E1, E2, N1, N2)  # Create a tuple representing the subset operation
        self.add_operation(operation)  # Add the operation to the list of operations
        wcps_query = self.generate_query()  # Generate the WCPS query based on added operations
        try:
            response = requests.post(self.dbc.url, data={'query': wcps_query}, verify=True)  # Send POST request
            response.raise_for_status()  # Raise an exception for HTTP errors
            img = Image.open(BytesIO(response.content))  # Open image from response content
            img.show()  # Display the image
            return response, wcps_query  # Return the response and WCPS query
        except (requests.exceptions.RequestException, IOError) as e:
            raise RuntimeError(f"Error performing subset operation: {e}")  # Raise an error if operation fails

    def subset_temperature(self, region, time_range):
        """Perform subset operation to retrieve temperature data."""
        operation = (f"Temperature_{region}", time_range, -180, 180, -90, 90)  # Create temperature subset operation
        self.add_operation(operation)  # Add the operation to the list of operations
        wcps_query = self.generate_query()  # Generate the WCPS query based on added operations
        try:
            response = requests.post(self.dbc.url, data={'query': wcps_query}, verify=True)  # Send POST request
            response.raise_for_status()  # Raise an exception for HTTP errors
            img = Image.open(BytesIO(response.content))  # Open image from response content
            img.show()  # Display the image
            return response, wcps_query  # Return the response and WCPS query
        except (requests.exceptions.RequestException, IOError) as e:
            raise RuntimeError(f"Error retrieving temperature data: {e}")  # Raise an error if operation fails

    def avg_temperature(self, region, time_range):
        """Calculate average temperature for a specific region and time range."""
        # Construct WCPS query to calculate average temperature
        wcps_query = f'''
        for $c in (Temperature_{region})
        return 
            avg($c[ansi("{time_range}")])
        '''
        result = self.execute_query(wcps_query)  # Execute the WCPS query
        if result:
            return result  # Return the result if successful
        else:
            raise RuntimeError("Error calculating average temperature.")  # Raise an error if calculation fails
        
    # Find maximum temperature for a specific region and time range.
    def max_temperature(self, region, time_range):
        wcps_query = f'''
        for $c in (Temperature_{region})
        return 
            max($c[ansi("{time_range}")])
        '''
        result = self.execute_query(wcps_query)  #
        result = self.execute_query(wcps_query)  # Execute the WCPS query
        if result:
            return result  # Return the result if successful
        else:
            raise RuntimeError("Error finding maximum temperature.")  # Raise an error if calculation fails
        
    # Find minimum temperature for a specific region and time range.
    def min_temperature(self, region, time_range):
        
        wcps_query = f'''
        for $c in (Temperature_{region})
        return 
            min($c[ansi("{time_range}")])
        '''
        result = self.execute_query(wcps_query)  # Execute the WCPS query
        if result:
            return result  # Return the result if successful
        else:
            raise RuntimeError("Error finding minimum temperature.")  # Raise an error if calculation fails

    def temperature_anomalies(self, region, time_range):
        """Find temperature anomalies for a specific region and time range."""
        # Construct WCPS query to find temperature anomalies
        wcps_query = f'''
        for $c in (Temperature_{region})
        return 
            $c[ansi("{time_range}")] - avg($c[ansi("{time_range}")])
        '''
        result = self.execute_query(wcps_query)  # Execute the WCPS query
        if result:
            return result  # Return the result if successful
        else:
            raise RuntimeError("Error finding temperature anomalies.")  # Raise an error if calculation fails
        
    # Calculate standard deviation for a specific coverage, region, and time range.
    def std_deviation(self, coverage, region, time_range):
        wcps_query = f'''
        for $c in ({coverage}_{region})
        return 
            stddev($c[ansi("{time_range}")])
        '''
        result = self.execute_query(wcps_query)  # Execute the WCPS query
        if result:
            return result  # Return the result if successful
        else:
            raise RuntimeError("Error calculating standard deviation.")  # Raise an error if calculation fails
        
    # Gives us a subset of temperature data for a specific location for certain period
    def get_subset_for_date_range(self, lat, long, start_date, end_date):
        return f"""
        for $c in ({self.coverage}) 
        return encode($c[Lat({lat}), Long({long}), ansi("{start_date}":"{end_date}")], "text/csv")
        """
    
    # Number of times the temperature at a specific location has been above the threshold 
    def count_occurrences_above_threshold(self, lat, long, start_time, end_time, threshold):
        return f"""
        for $c in ({self.coverage}) 
        return count($c[Lat({lat}), Long({long}), ansi("{start_time}":"{end_time}")] > {threshold})
        """
    
    #Convert operation tuple to WCPS query string.
    def to_wcps(self, operation):
        return f"$c[ansi(\"{operation[1]}\"), E({operation[2]}:{operation[3]}),N({operation[4]}:{operation[5]})],"
