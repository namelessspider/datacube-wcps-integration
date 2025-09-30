from wdc.dbc_connection import dbc
from wdc.dbo_datacube import dbo


server_url = "https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage"
dc_connection = dbc(server_url)
coverage = 'AvgLandTemp'
dc_object = dbo(dc_connection, coverage)
lat_start = 35
lat_end = 75
lon_start = -20
lon_end = 40
ansi_start = "2014-07"

query = dc_object.on_the_fly_colouring(lat_start, lat_end, lon_start, lon_end, ansi_start)
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