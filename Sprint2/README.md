## Group 38 Software Engineering Project (Sprint 2)

Authors of the code:
1) Elene Esakia
2) Timur Malanin

In this repository, we recreated previously written funcs.py file and created a new Python library (wdc) designed to simplify interaction with a Web Coverage Processing Service (WCPS) server. It provides intuitive interfaces for establishing database connections, managing datacubes, and executing WCPS queries. With wdc, users can seamlessly generate queries, compose custom queries, and execute them efficiently on the server via a datacube object.

## Repository Structure

To adhere to best practices and ensure a well-organized codebase, we have restructured the repository. Taking inspiration from established open-source Python libraries, we have implemented a more organized layout with separate folders for different types of files. In the directory we added two folders: wdc library and tests folder.

```
 Group 38's project/
 │
 ├── wdc/
 │    ├── __init__.py
 │    ├── dbc_connection.py
 │    ├── dbo_datacube.py
 │   
 ├── tests/
 │    ├── __init__.py
 │    ├── test.py
 │    ├── example_query.py
 │    ├── test_sprint_2.py
 │
 └── README.md
```


- wdc/: This directory contains the source code for the wdc library.
  - __init__.py: Initialization file to make the directory a Python package.
  - dbc_connection.py: Implementation of the Database Connection Object (dbc).
  - dbo_datacube.py: Implementation of the Datacube Object (dbo).
- tests/: This directory houses all unit tests for the wdc library.
  - __init__.py: Initialization file to make the directory a Python package.
  - test.py: Main test file containing test cases for the wdc library.
  - example_query.py: Additional test file containing example queries for reference.
  - test_sprint_2.py: New test file containing test cases for the new methods we added to the wdc library.
- README.md: The main README file providing an overview of the project.

## New Functionality

We have added some additional functionality other than the functions provided in the funcs.py file to the dbo_datacube.py file:

- Fetch Metadata: Retrieves metadata about the dataset from the server.
- Detect Anomalies: Generates a query to detect anomalies in the dataset over a specified time period at a given location.
- Zonal Statistics: Generates a query for zonal statistics over a specified geographic area and time period.
- Export Data: Generates a query to export data in a specified format (CSV or JSON).
  
### Instructions/sample usage:

```
# Import all the necessary libraries
from wdc.dbc_connection import dbc
from wdc.dbo_datacube import dbo

# Define the URL of the server you want to connect to
server_url = "https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage"

# Create a dbc object by passing the server URL
dbc_connection = dbc(server_url)

# Specify the coverage you want to work with
coverage = 'AvgLandTemp'

# Create a dbo object by passing the connection and coverage
dbo_object = dbo(dbc_connection, coverage)

# Provide necessary parameters for the query
lat = 53.08
lon = 8.80
ansi_start = "2014-04-02"
ansi_end = "2014-09-11"

# Utilize the provided methods within the dbo class to construct your queries
query = dbo_object.maximum(lat=lat, lon=lon, ansi_start=ansi_start, ansi_end=ansi_end)

# Execute the query using the execute_query method of the dbc object
result = dbc_connection.execute_query(query=query)

# Store or utilize the result as needed
print(result)
```

### Testing:

Below is a sample code snippet demonstrating a test for one of many provided functions to make heatmap of specified locations at a specific time.

```python
from wdc import dbc, dbo

server_url = "https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage"
dc_connection = dbc(server_url)
coverage = 'AvgLandTemp'
dc_object = dbo(dc_connection, coverage)
lat_start = 35
lat_end = 75
lon_start = -20
lon_end = 40
ansi_start = "2014-07"

query = dc_object.on_the_fly_colouring(lat_start, lat_end, lon_start, lon_end, ansi)
result = dc_connection.execute_query(query=query)

expected_query = """
image>>for $c in ( AvgLandTemp ) 
        return encode(
            switch 
                    case $c[ansi("2014-07"), Lat(35:75), Long(-20:40)] = 99999 
                        return {red: 255; green: 255; blue: 255}
                    case 18 > $c[ansi("2014-07"), Lat(35:75), Long(-20:40)] 
                        return {red: 0; green: 0; blue: 255} 
                    case 23 > $c[ansi("2014-07"), Lat(35:75), Long(-20:40)] 
                        return {red: 255; green: 255; blue: 0} 
                    case 30 > $c[ansi("2014-07"), Lat(35:75), Long(-20:40)]  
                        return {red: 255; green: 140; blue: 0}
                    default return {red: 255; green: 0; blue: 0}
                , "image/png")
"""

assert query.strip() == expected_query.strip(), "Test Case Failed"
print("'on_the_fly_colouring' function Test Case Passed\n")
```

The test passes and displays an appropriate message to indicate the success. By passing this query, you will get the following heatmap as a result:

<img src='./sprint_1/wdc/assets/heatmap.png' width='100%' >

