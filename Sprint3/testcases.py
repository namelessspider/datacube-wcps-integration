import unittest
from wdc.Connection import dbc
from wdc import Query, Params

server_url = "https://ows.rasdaman.org/rasdaman/ows"
db_conn = dbc(server_url=server_url)

class TestQueries(unittest.TestCase):
    def testMostBasicQuery(self):
        query = Query("AvgLandTemp")
        query.set_query_type("most_basic_query")
        result = db_conn.execute_query(query.get_wcps())
        self.assertEqual(result, b'1', "Test case failed: Expected result '1' but got '{}'".format(result.decode()))

    def testSelectingSingleValue(self):
        query = Query("AvgLandTemp")
        query.set_query_type("selecting_single_value")
        ansiSubset = Params("ansi", "2014-07")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = db_conn.execute_query(query.get_wcps())
        self.assertEqual(result, b'25.984251', "Test case failed")

    def test3Dto1D(self):
        query = Query("AvgLandTemp")
        query.set_query_type("transform_3d_to_1d_subset")
        ansiSubset = Params("ansi", "2014-01", "2014-12")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = query.get_wcps()
        expected_result = '''diagram>>for $c in ( AvgLandTemp )
 return encode(
$c[ansi("2014-01":"2014-12"), Lat(53.08), Long(8.8)]
, "text/csv")'''
        self.assertEqual(result, expected_result, "Test case failed")

    def test3Dto2D(self):
        query = Query("AvgTemperatureColorScaled")
        query.set_query_type("transform_3d_to_2d_subset")
        ansiSubset = Params("ansi", "2014-07")
        query.set_params([ansiSubset])
        result = query.get_wcps()
        expected_result = '''image>>for $c in ( AvgTemperatureColorScaled )
 return encode(
$c[ansi("2014-07")]
, "image/png")'''
        self.assertEqual(result, expected_result, "Test case failed")

    def testCelsToKelv(self):
        query = Query("AvgLandTemp")
        query.set_query_type("celsius_to_kelvin")
        ansiSubset = Params("ansi", "2014-01", "2014-12")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = query.get_wcps()
        expected_result = '''diagram>>for $c in ( AvgLandTemp )
 return encode(
$c[ansi("2014-01":"2014-12"), Lat(53.08), Long(8.8)]
+273.15
, "text/csv")'''
        self.assertEqual(result, expected_result, "Test case failed")

    def testMin(self):
        query = Query("AvgLandTemp")
        query.set_query_type("min")
        ansiSubset = Params("ansi", "2014-01", "2014-12")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = db_conn.execute_query(query.get_wcps())
        expected_result = b'2.2834647'
        self.assertEqual(result, expected_result, "Test case failed")

    def testMax(self):
        query = Query("AvgLandTemp")
        query.set_query_type("max")
        ansiSubset = Params("ansi", "2014-01", "2014-12")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = db_conn.execute_query(query.get_wcps())
        expected_result = b'25.984251'
        self.assertEqual(result, expected_result, "Test case failed")

    def testAvg(self):
        query = Query("AvgLandTemp")
        query.set_query_type("avg")
        ansiSubset = Params("ansi", "2014-01", "2014-12")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = db_conn.execute_query(query.get_wcps())
        expected_result = b'15.052493472894033'
        self.assertEqual(result, expected_result, "Test case failed")

    def testMoreThan15(self):
        query = Query("AvgLandTemp")
        query.set_query_type("when_temp_more_than_15")
        ansiSubset = Params("ansi", "2014-01", "2014-12")
        latSubset = Params("Lat", 53.08)
        longSubset = Params("Long", 8.80)
        query.set_params([ansiSubset, latSubset, longSubset])
        result = db_conn.execute_query(query.get_wcps())
        expected_result = b'7'
        self.assertEqual(result, expected_result, "Test case failed")

if __name__ == '__main__':
    unittest.main()
