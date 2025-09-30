## Group 39's Sprint 3 Software Engineering Project

This repository contains functions developed by Group 39 for their sprint 3 software engineering project. These functions are designed to handle connections with a datacube server, execute queries to retrieve specific data, and provide real-time feedback on the connection status.

### Instructions:

1. **Import the Necessary Classes:**

   ```python
   from wdc import dbc, Query, Params
   ```

2. **Set Up Server Connection:**

   - Define the URL of the server you want to connect to.
   - Create a `dbc` object by passing the server URL.
     ```python
     server_url = "https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage"
     dbc_connection = dbc(server_url)
     ```

3. **Create Query Object:**

   - Specify the coverage you want to work with (for the sake of this example, we will be using AvgLandTemp)
   - Create a `Query` object, specifying the coverage and then the query type (we will use selecting_single_value for this example).
     ```python
     query = Query("AvgLandTemp")
     query.set_query_type("selecting_single_value")
     ```

4. **Set Query Parameters:**

   - Define the parameters required for the query (ansi, latitude, longitude)
   - Create `Params` objects and add them to the query using the `.set_params` method.
     ```python
     ansi_subset = Params("ansi", "2014-07")
     lat_subset = Params("Lat", 53.08)
     long_subset = Params("Long", 8.80)
     ```

5. **Generate WCPS Query:**
   - Get the WCPS query string from the constructed query object.
     ```python
     wcps_query = query.get_wcps()
     ```
6. **New Arbitrary Queries:**

   - Added private methods _apply_operation, _apply_subset, _apply_scale, and encode_format for supporting various operations.
   - Additional query types and return types have been included for more versatile query generation.
   - Methods have been refactored for improved readability and organization.

### Modifications that we made in the 3rd sprint:

### Execute Queries:

To execute a query, call the execute_query method of the dbc_connection object and pass the WCPS query as a parameter. If the connection is successful, it will print "Connection successful!" to the terminal. If the connection fails, it will print an appropriate error message.

result = dbc_connection.execute_query(wcps_query)
print(result)
`

### Get All Possible Coverages:

To retrieve a list of all available coverages from the rasdaman server, use the
`get_all_possible_coverages` method of the `dbc_connection` object. If the connection is
successful, it will print "Connection successful!" to the terminal. If the connection
fails, it will print an appropriate error message.

```python
 all_coverages = dbc_connection.get_all_possible_coverages()
 print("Available coverages:", all_coverages)
```

By adding these modifications, the code now provides feedback in the terminal indicating - whether the connection to the server was successful or not. This enhances user experience by providing real-time status updates.


This markdown-style README provides clear instructions on how to use the functions developed in sprint 3, including setting up the server connection, executing queries, and retrieving available coverages.

### Changes Made in terms of Testing:

1. **Migration to Unittest Framework**:

   - Tests now utilize the Unittest framework for improved organization and reporting.

2. **Test Case Refactoring**:

   - Test cases now use Unittest's assertion methods for better readability and failure reporting.

3. **Test Organization**:

   - All tests are organized within a single `TestQueries` class, making it easier to manage and execute.

4. **Improved Test Reporting**:
   - Unittest's reporting features provide detailed summaries of test results.

### Instructions for Running Tests:

To execute the tests:

1. Ensure dependencies are installed.
2. Run `python test_queries.py` in the project directory. 
  
### Sample Usage:

Below is a sample code snippet demonstrating the usage of the provided functions to execute the `selecting_single_value` WCPS query.

```python
from wdc import dbc, Query, Params

server_url = "https://ows.rasdaman.org/rasdaman/ows"

conn = dbc(server_url)

query = Query("AvgLandTemp")
query.set_query_type("selecting_single_value")

ansiSubset = Params("ansi", "2014-07")
latSubset = Params("Lat", 53.08)
longSubset = Params("Long", 8.80)
query.set_params([ansiSubset, latSubset, longSubset])

wcps_query = query.get_wcps()
```

### Image Generation

Below is a sample image generated when running the `3d to 2d subset transform` on the `AvgTemperatureColorScaled` coverage
![image](https://github.com/Constructor-Uni-SE-non-official/Sprint2_Pair39/assets/145987692/08ca34f0-0bb1-45a4-93ae-c2cb021c9ada)


### Authors:
- Elene Esakia
- Ani Nikoladze-Janiashvili
