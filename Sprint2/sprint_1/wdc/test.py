"""
Group 38's sprint 1 software engineering project's function tests
"""
from sprint_1.wdc import dbc, dbo

# dbc = Database Connection
# dbo = Database Object

"""
Using dbc class functions to connect to the WCPS server through the 'server_url'
Using dbo class functions to create a Datacube object for the 'AvgLandTemp' coverage

All tests executed with predetermined parameters for which results and queries are known
"""
server_url = 'https://ows.rasdaman.org/rasdaman/ows?Rexpected_queryUEST=GetCoverage'  # Link used for connection to WCPS server - Gets Coverages for the user
db_conn = dbc(server_url)
db_obj = dbo(db_conn, "AvgLandTemp")


# Testing the most_basic_query function (comparing results)
query = db_obj.most_basic_query()
result = db_conn.execute_query(query)

assert result == b'1', "Test Case Failed"
print("'most_basic_query' function Test Case Passed\n")


# Testing the selecting_single_value function (comparing results)
query = db_obj.selecting_single_value(53.08, 8.80, '2014-01')
result = db_conn.execute_query(query)

assert result == b'2.8346457', "Test Case Failed"
print("'selecting_single_value' function Test Case Passed\n")


# Testing the transform_3d_to_1d_subset function (comparing queries)
query = db_obj.transofrm_3d_to_1d_subset(53.08, 8.80, "2014-01", "2014-12")

expected_query= """
diagram>>for $c in ( AvgLandTemp )
        return encode(
                    $c[Lat(53.08), Long(8.8]), ansi("2014-01":"2014-12")]
                , "text/csv")
"""
assert expected_query.strip() == query.strip(), "Test Case Failed"
print("'transform_3d_to_1d_subset' function Test Case Passed\n")


# Testing the transform_3d_to_2d_subset function (comparing queries)
query = db_obj.transform_3d_to_2d_subset("2014-01")

expected_query = """
image>>for $c in ( AvgLandTemp )
         return encode(
                       $c[ansi(2014-01)]
                , "image/png")
"""

assert expected_query.strip() == query.strip(), "Test Case Failed"
print("'transform_3d_to_2d_subset' function Test Case Passed\n")


# Testing the celsius_to_kelvin function (comparing results)
query = db_obj.celsius_to_kelvin(53.08, 8.80, "2014-01", "2014-12")
result = db_conn.execute_query(query)

expected = b'275.9846457481384,277.6381887435913,284.2523626327514,293.346849822998,294.1736225128174,294.4492134094238,299.1342510223388,297.4807094573974,295.2759841918945,289.2129920959472,282.0476373672485,275.4334646701813'

assert result == expected, "Test Case Failed"
print("'celsius_to_kelvin' function Test Case Passed\n")


# Testing the minimum function (comparing results)
query = db_obj.minimum(53.08, 8.80, "2014-01", "2014-12")
result = db_conn.execute_query(query)

expected = b'2.2834647'

assert result == expected, "Test Case Failed"
print("'minimum' function Test Case Passed\n")


# Testing the maximum function (comparing results)
query = db_obj.maximum(53.08, 8.80, "2014-01", "2014-12")
result = db_conn.execute_query(query)

expected = b'25.984251'

assert result == expected, "Test Case Failed"
print("'maximum' function Test Case Passed\n")


# Testing the average function (comparing results)
query = db_obj.average(53.08, 8.80, "2014-01", "2014-12")
result = db_conn.execute_query(query)

expected = b'15.052493472894033'

assert result == expected, "Test Case Failed"
print("'average' function Test Case Passed\n")


# Testing the on_the_fly_colouring function (comparing queries)
query = db_obj.on_the_fly_colouring(35, 75, -20, 40, "2014-07")

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


# Testing the coverage_constructor function (comparing queries)
query = db_obj.coverage_constructor("myCoverage", 0, 200, 0, 200)

expected_query = """
image>>for $c in ( AvgLandTemp ) 
        return encode(
                        coverage myCoverage
                        over $p x(0:200),
                            $q y(0:200)
                        values $p + $q
            , "image/png")
"""

assert expected_query.strip() == query.strip(), "Test Case Failed"
print("'coverage_constructor' function Test Case Passed\n")