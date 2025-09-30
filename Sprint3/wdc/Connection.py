from typing import Union, List, BinaryIO, NewType
import requests
from requests import HTTPError
import xml.etree.ElementTree as ET

# Defining custom types for return type hinting
Image = NewType('Image', BinaryIO)
Diagram = NewType('Diagram', BinaryIO)
Query = NewType('Query', str)

class dbc:
    """
    A class responsible for connecting to the rasdaman server of the datacube.

    Attributes
    ----------
    server_url : str
        URL of the server to connect to.

    Methods
    -------
    __init__(self, server_url: str)
        Initializes the dbc object with the provided server URL.
    
    execute_query(self, query: Query) -> Union[int, float, bytes, str, Image, Diagram]
        Executes a query on the rasdaman server and returns the result.
    
    get_all_possible_coverages(self) -> List[str]
        Retrieves a list of all available coverages from the rasdaman server.
    """

    def __init__(self, server_url: str):
        """
        Initializes the dbc object with the provided server URL.

        Parameters
        ----------
        server_url : str
            URL of the server to connect to.

        Returns
        -------
        None
        """
        self.url = server_url

    def execute_query(self, query: Query) -> Union[int, float, Image, Diagram]:
        """
        Args:
            query (str): The query that was built to be executed by user

        Returns:
            Union[int, float, Image, Diagram]: All possible return types for a query
        """
        try:
            response = requests.post(self.url, {'query': query})
            response.raise_for_status()  # Raises HTTP error
            print("Connection successful!")  # Add this line to indicate success
            return response.content
        except HTTPError as err:
            print(f"Connection failed: {err}")  # Add this line to indicate failure
            if response.status_code == 500:
                return f"The server encountered an error and could not process your request: {err}"
            else:
                return f"The page isn't working right now. Please try again: {err}"
        except Exception as exc:
            print(f"An unexpected error has occurred: {exc}")  # Add this line to indicate failure
            return f"An unexpected error has occurred: {exc}"

    def get_all_possible_coverages(self) -> List[str]:
        """
        Retrieves a list of all available coverages from the rasdaman server.

        Returns
        -------
        List[str]
            A list of strings representing the names of all available coverages.
        """
        get_capabilities_url = "https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&VERSION=2.1.0&REQUEST=GetCapabilities"
        response = requests.post(get_capabilities_url)
        if response.status_code == 200:
            print("Connection successful!")  # Add this line to indicate success
        else:
            print(f"Connection failed: {response.status_code}")  # Add this line to indicate failure
        coverage_names = []
        root = ET.fromstring(response.content)
        namespaces = {'wcs20': 'http://www.opengis.net/wcs/2.0'}
        for coverage in root.findall(".//wcs20:CoverageId", namespaces):
            coverage_names.append(coverage.text)
        return coverage_names


# Finding all coverages to validate coverages users wish to use (applied in wdc/Query.py)
obj = dbc("https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage")
allCoverages = obj.get_all_possible_coverages()
print("Available coverages:", allCoverages)
