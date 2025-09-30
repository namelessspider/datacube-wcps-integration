# Software Engineering Project
### Sprint 1 Details:

The Datacube Operations Library is a Python package designed to interact with Web Coverage Processing Service (WCPS) servers. WCPS is a standard for querying and processing multi-dimensional raster data, commonly referred to as datacubes.

### Key Features:
These are the key features we have implemented during the first sprint:
1. **Subset Operations:**
   - The library allows users to extract subsets of data from a datacube based on spatial and temporal criteria. Users can specify the region of interest using latitude and longitude coordinates and define the time range for the subset.

2. **Statistical Calculations:**
   - We implemented statistical calculations on datacubes, including calculating averages, maximum and minimum values, and standard deviations. These calculations can be applied to specific regions and time ranges within the datacube.

3. **Temperature Anomalies:**
   - We also included functionality to compute temperature anomalies for specific regions and time ranges. This enables users to identify deviations from expected temperature patterns within the data.

4. **Connection Handling:**
   - Robust connection handling is implemented to ensure reliable communication with WCPS servers. Users can configure timeout durations and the number of retry attempts to accommodate varying network conditions.

### Usage:

1. **Initialization:**
   - Users initialize a `DatabaseConnection` object by providing the URL of the WCPS server. This object facilitates communication with the server and handles connection-related tasks.

2. **Datacube Operations:**
   - After initializing a `DatabaseConnection`, users create a `Datacube` object using the connection. This object serves as a container for performing operations on the datacube.
   - Operations such as subset extraction, statistical calculations, and anomaly detection are added to the `Datacube` object using its methods.

3. **Execution:**
   - Once operations are added, users generate a WCPS query string representing the desired operations. The library handles the execution of the query on the WCPS server and returns the results to the user.

This summary provides an overview of what we did during Sprint 1. It does not show any code. 
