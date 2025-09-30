import unittest

from wdc.dbc_connection import dbc
from wdc.dbo_datacube import dbo


class TestDatabaseOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server_url = 'https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage'
        cls.db_conn = dbc(server_url)
        cls.db_obj = dbo(cls.db_conn, "AvgLandTemp")

    def test_fetch_metadata(self):
        expected_query = "metadata>>for $c in ( AvgLandTemp ) return encode(properties($c), 'application/json')"
        query = self.db_obj.fetch_metadata()
        self.assertEqual(query, expected_query, "Fetch metadata function Test Case Failed")

    def test_detect_anomalies(self):
        query = self.db_obj.detect_anomalies(34.05, -118.25, '20210101', '20210131')
        expected_query = """
        for $c in (AvgLandTemp)
        return
            filter(anomaly_detection($c[Lat(34.05), Long(-118.25), ansi("20210101":"20210131")]), threshold > 3)
        """
        self.assertEqual(query.strip(), expected_query.strip(), "Detect anomalies function Test Case Failed")

    def test_zonal_statistics(self):
        query = self.db_obj.zonal_statistics(30, 35, -120, -115, '20210101', '20210131')
        expected_query = """
        for $c in (AvgLandTemp)
        return
            stats($c[Lat(30:35), Long(-120:-115), ansi("20210101":"20210131")])
        """
        self.assertEqual(query.strip(), expected_query.strip(), "Zonal statistics function Test Case Failed")

    def test_export_data(self):
        query = self.db_obj.export_data('csv')
        expected_query = """
        for $c in (AvgLandTemp)
        return
            encode($c, "csv")
        """
        self.assertEqual(query.strip(), expected_query.strip(), "Export data function Test Case Failed")

    # Existing test methods...
    # Continue to add existing test methods here.

if __name__ == '__main__':
    unittest.main()
