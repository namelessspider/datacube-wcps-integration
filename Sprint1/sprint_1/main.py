from dco import Datacube  
from dbc import DatabaseConnection  

url = 'https://ows.rasdaman.org/rasdaman/ows'

# Create a DatabaseConnection instance
dbc = DatabaseConnection(url)

# Create a Datacube instance
datacube = Datacube(dbc)

# Test subset_temperature method
def test_subset_temperature():
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        response, wcps_query = datacube.subset_temperature(region, time_range)
        print("Subset temperature operation successful.")
    except Exception as e:
        print(f"Error in subset_temperature method: {e}")

# Test avg_temperature method
def test_avg_temperature():
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.avg_temperature(region, time_range)
        print(f"Average temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in avg_temperature method: {e}")

# Test max_temperature method
def test_max_temperature():
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.max_temperature(region, time_range)
        print(f"Maximum temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in max_temperature method: {e}")

# Test min_temperature method
def test_min_temperature():
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.min_temperature(region, time_range)
        print(f"Minimum temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in min_temperature method: {e}")

# Test temperature_anomalies method
def test_temperature_anomalies():
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.temperature_anomalies(region, time_range)
        print(f"Temperature anomalies for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in temperature_anomalies method: {e}")

# Test std_deviation method
def test_std_deviation():
    try:
        coverage = "Temperature"  
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.std_deviation(coverage, region, time_range)
        print(f"Standard deviation for {coverage}_{region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in std_deviation method: {e}")

# Run the test methods
test_subset_temperature()
test_avg_temperature()
test_max_temperature()
test_min_temperature()
test_temperature_anomalies()
test_std_deviation()
