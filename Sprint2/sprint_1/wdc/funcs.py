"""
Group 38's sprint 1 software engineering project's functions
"""

# imported typing for typehints
from typing import Union, NewType, BinaryIO
import requests
from requests import HTTPError


# Defining image as a type for return typehinting
Image = NewType('Image', BinaryIO)
Diagram = NewType('Diagram', BinaryIO)


class dbc:
    """
    A class used to handle connection with the server whose URL was given


    Attributes
    ----------
    server_url : str
        URL of the server user wants to connect to


    Methods
    -------
    __init__(self, server_url: str) -> Union[bytes, str]:
        Function that initialises the connection to the server whose url was provided
        and returns either bytes (response.content) or a string (error
        message)

    get_capabilities(self):
        Function that returns all possible coverages user can use

    execute_query(self, query: str) -> Union[int, float, Image, Diagram]:
        Function to execute the query the user provides and the result of
        the query is either an integer, float, image or diagram
    """

    def __init__(self, server_url: str):
        """
        Parameters
        ----------
        server_url : str
            URL of the server user wants to connect to

        possible_coverages : str
            All possible coverages we can use
        """
        self.url = server_url
        self.coverages = ['AvgLandTemp']

    def get_capabilities(self):
        return self.coverages

    def execute_query(self, query: str) -> Union[int, float, Image, Diagram]:
        """
        Args:
            query (str): The query that was built to be executed by user

        Returns:
            Union[int, float, Image, Diagram]: All possible return types for a query
        """

        try:
            """
            Attempting to connect to the server whose URL was provided and 
            posting a query
            """
            response = requests.post(self.url, {'query':query})
            response.raise_for_status() # Raises HTTP error

        except HTTPError as err:
            """
            Handling all possible server or user errors while connecting 
            and providing an appropriate response
            """
            # A status code of 500 implies an issue with the server and not user
            if response.status_code == 500:
                return f"The server encountered an error and could not process your request: {err}"

            # If it is not an issue with the server, it is an issue with the user
            else:
                return f"The page isn't working right now. Please try again: {err}"

        except Exception as exc:
            """
            Handling any exceptions and displaying appropriate error
            message
            """
            return f"An unexpected error has occurred: {exc}"

        return response.content


class dbo:
    """
    A class of the datacube connection object that handles all queries and
    communications with the server


    Attributes
    ---------
    connection : dbc
        The connection to the server
    coverage : str
        The coverage the user wishes to use


    Methods
    -------
    __init__(self, connection: dbc, coverage: str):
        Initialises the object, providing it with connection and coverage.

    most_basic_query(self, coverage: str) -> str:
        Function to handle query generation of most basic query, which
        returns 1 for every pixel in the provided coverage.

    selecting_single_value(self, lat: float, lon: float, ansi: str) -> str:
        Function to handle query generation of selecting single value, which
        returns the value at a specified point at a specified time.

    transform_3d_to_1d_subset(self, lat: float, lon: float, ansi: str) -> str:
        Function to handle query generation of 3d->1d subset which converts
        3-dimensional data into 1-dimensional data.

    transform_3d_to_2d_subset(self, lat: float, lon:float, ansi: str) -> str:
        Function to handle query generation of 3d->2d subset which converts
        3-dimensional data into 2-dimensional data

    celsius_to_kelvin(self, lat: float, lon: float, ansi: str) -> str:
        Function to convert temperature at a given point during a given time
        period from celsius to kelvin

    minimum(self, lat: float, lon: float, ansi: str) -> str:
        Function to get minimum value at the specified point from the given
        time period

    maximum(self, lat: float, lon: float, ansi: str) -> str:
        Function to get maximum value at the specified point from the given
        time period

    average(self, lat: float, lon: float, ansi: str) -> str:
        Function to get average value at the specified point from the given
        time period

    when_temp_more_than_15(self, lat: float, lon: float, ansi: str) -> str:
        Function to get number of times temperature was more than 15

    on_the_fly_colouring(self, lat_start: float, lat_end: float,
                             lon_start: float, ansi: str) -> str:
        Function to make heatmap of specified locations at a specific time


    Parameters
    ----------
    lat : float
        Latitude or range of latitudes of the specified point.
    lon : float
        Longitude or range of longitudes of the specified point.
    ansi : str
        The date or range of dates for which the user wants to receive data.
    """


    def __init__(self, connection: dbc, coverage: str):
        """
        Args:
            connection (dbc): the connection to the server
            coverage (str): the coverage the user wishes to use
        """
        self.connection = connection
        self.coverage = coverage if coverage in self.connection.get_capabilities() else None

        if self.coverage is None:
            raise ValueError("Invalid coverage. Please provide again")


    def most_basic_query(self) -> str:
        """
        Args:
            coverage (str): the coverage the user wishes to use

        Returns:
            str: the final query
        """

        return f"""
        for $c in ({self.coverage}) return 1
        """


    def selecting_single_value(self, lat: float, lon: float, ansi: str) -> str:
        """
        Args:
            lat (float): latitude of the specificied point
            lon (float): longitude of the specificied point
            ansi (str): the date for which the user wants to receive data of

        Returns:
            str: the final query
        """

        return f"""
        for $c in ({self.coverage})
        return $c[Lat({lat}), Long({lon}), ansi("{ansi}")]"""


    def transofrm_3d_to_1d_subset(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Function to handle query generation of 3d->1d subset which converts
        3-dimensional data into 1-dimensional data

        Args:
            lat (float): latitude of the specificied point
            lon (float): longitude of the specificied point
            ansi_start (str): start of the time the user wishes to record
            ansi_end (str): end of the time period the user wishes to record data

        Returns:
            str: the final query
        """

        return f"""
        diagram>>for $c in ( {self.coverage} )
        return encode(
                    $c[Lat({lat}), Long({lon}]), ansi("{ansi_start}":"{ansi_end}")]
                , "text/csv")"""


    def transform_3d_to_2d_subset(self, ansi: str) -> str:
        """
        Args:
            ansi (str): the date for which the user wishes to convert the data

        Returns:
            str: the final query
        """

        return f"""
        image>>for $c in ( {self.coverage} )
         return encode(
                       $c[ansi({ansi})]
                , "image/png")"""


    def celsius_to_kelvin(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Args:
            lat (float): latitude of speicified point
            lon (float): longitude of specified point
            ansi_start (str): start of the time the user wishes to record
            ansi_end (str): end of the time period the user wishes to record data

        Returns:
            str: the final query
        """

        return f"""
        diagram>>for $c in ( {self.coverage} ) 
         return encode(
                        $c[Lat({lat}), Long({lon}), ansi("{ansi_start}":"{ansi_end}")] 
                        + 273.15
                , "text/csv")"""


    def minimum(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Args:
            lat (float): latitude of speicified point
            lon (float): longitude of specified point
            ansi_start (str): start of the time the user wishes to record
            ansi_end (str): end of the time period the user wishes to record data

        Returns:
            str: the final query
        """

        return f"""
        for $c in ({self.coverage}) 
        return 
            min($c[Lat({lat}), Long({lon}), ansi("{ansi_start}":"{ansi_end}")])"""


    def maximum(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Args:
            lat (float): latitude of speicified point
            lon (float): longitude of specified point
            ansi_start (str): start of the time the user wishes to record
            ansi_end (str): end of the time period the user wishes to record data

        Returns:
            str: the final query
        """

        return f"""
        for $c in ({self.coverage}) 
        return 
            max($c[Lat({lat}), Long({lon}), ansi("{ansi_start}":"{ansi_end}")])"""


    def average(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Args:
            lat (float): latitude of speicified point
            lon (float): longitude of specified point
            ansi_start (str): start of the time the user wishes to record
            ansi_end (str): end of the time period the user wishes to record data

        Returns:
            str: the final query
        """

        return f"""
        for $c in ({self.coverage}) 
        return 
            avg($c[Lat({lat}), Long({lon}), ansi("{ansi_start}":"{ansi_end}")])"""


    def when_temp_more_than_15(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Args:
            lat (float): latitude of speicified point
            lon (float): longitude of specified point
            ansi_start (str): start of the time the user wishes to record
            ansi_end (str): end of the time period the user wishes to record data

        Returns:
            str: the final query
        """

        return f"""
        for $c in (AvgLandTemp)
        return count(
                        $c[Lat({lat}), Long({lon}), ansi("{ansi_start}":"{ansi_end}")]
                    > 15)"""


    def on_the_fly_colouring(self, lat_start: float, lat_end: float,
                             lon_start: float, lon_end: float, ansi: str) -> str:
        """
        Args:
            lat_start (float): starting value of the range of latitudes
            lat_end (float): ending value of the range of latitudes
            lon_start (float): starting value of range of longitudes
            lon_end (float): ending value of range of longitudes
            ansi (str): the specific date for which the user wants to see the heatmap

        Returns:
            str: the final query
        """

        return f"""
        image>>for $c in ( AvgLandTemp ) 
        return encode(
            switch 
                    case $c[ansi("{ansi}"), Lat({lat_start}:{lat_end}), Long({lon_start}:{lon_end})] = 99999 
                        return {{red: 255; green: 255; blue: 255}}
                    case 18 > $c[ansi("{ansi}"), Lat({lat_start}:{lat_end}), Long({lon_start}:{lon_end})] 
                        return {{red: 0; green: 0; blue: 255}} 
                    case 23 > $c[ansi("{ansi}"), Lat({lat_start}:{lat_end}), Long({lon_start}:{lon_end})] 
                        return {{red: 255; green: 255; blue: 0}} 
                    case 30 > $c[ansi("{ansi}"), Lat({lat_start}:{lat_end}), Long({lon_start}:{lon_end})]  
                        return {{red: 255; green: 140; blue: 0}}
                    default return {{red: 255; green: 0; blue: 0}}
                , "image/png")"""


    def coverage_constructor(self, coverage_name: str, x_min: float,
                             x_max: float, y_min: float, y_max: float) -> str:
        """
        Args:
            coverage_name (str): name for the new coverage user is defining
            x_min (float): minimum value for horizontal extent of coverage
            x_max (float): maximum value for horizontal extent of coverage
            y_min (float): minimum value for vertical extent of coverage
            y_max (float): maximum value for vertical extent of coverage

        Returns:
            str: the final query
        """

        return f"""
        image>>for $c in ( {self.coverage} ) 
        return encode(
                        coverage {coverage_name}
                        over $p x({x_min}:{x_max}),
                            $q y({y_min}:{y_max})
                        values $p + $q
            , "image/png")"""
    def fetch_metadata(self) -> str:
        """
        Retrieves metadata about the dataset from the server.

        Returns:
            str: Query for fetching dataset metadata.
        """
        return f"metadata>>for $c in ( {self.coverage} ) return encode(properties($c), 'application/json')"

    def detect_anomalies(self, lat: float, lon: float, ansi_start: str, ansi_end: str) -> str:
        """
        Generates a query to detect anomalies in the dataset over a specified time period at a given location.

        Args:
            lat (float): Latitude of the specified point.
            lon (float): Longitude of the specified point.
            ansi_start (str): Start of the time period.
            ansi_end (str): End of the time period.

        Returns:
            str: the final query for detecting anomalies.
        """
        return f"""
        for $c in ({self.coverage})
        return
            filter(anomaly_detection($c[Lat({lat}), Long({lon}), ansi("{ansi_start}":"{ansi_end}")]), threshold > 3)
        """

    def zonal_statistics(self, lat_start: float, lat_end: float, lon_start: float, lon_end: float, ansi_start: str,
                         ansi_end: str) -> str:
        """
        Generates a query for zonal statistics over a specified geographic area and time period.

        Args:
            lat_start (float): Starting latitude.
            lat_end (float): Ending latitude.
            lon_start (float): Starting longitude.
            lon_end (float): Ending longitude.
            ansi_start (str): Start of the time period.
            ansi_end (str): End of the time period.

        Returns:
            str: The final query for zonal statistics.
        """
        return f"""
        for $c in ({self.coverage})
        return
            stats($c[Lat({lat_start}:{lat_end}), Long({lon_start}:{lon_end}), ansi("{ansi_start}":"{ansi_end}")])
        """

    def export_data(self, format: str = 'csv') -> str:
        """
        Generates a query to export data in a specified format.

        Args:
            format (str): Desired format ('csv' or 'json').

        Returns:
            str: The final query to export data.
        """
        return f"""
        for $c in ({self.coverage})
        return
            encode($c, "{format}")
        """
