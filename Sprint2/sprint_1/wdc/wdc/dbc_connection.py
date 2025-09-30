import requests
from requests import HTTPError
from typing import Union, NewType, BinaryIO

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