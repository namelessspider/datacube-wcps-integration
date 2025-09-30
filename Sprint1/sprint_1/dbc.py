import requests
import logging

class DatabaseConnection:
    def _init_(self, url, timeout=10, max_retries=3):
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

        try:
            self._establish_connection()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to establish a connection to the server: {e}")

    def _establish_connection(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = requests.get(self.url, timeout=self.timeout)
                response.raise_for_status()  # Raise an exception for HTTP errors
                self.logger.info("Connection to the server established successfully!")
                return
            except requests.exceptions.RequestException as e:
                self.logger.warning("Connection attempt failed: %s", e)
                retry_count += 1
        raise ConnectionError(f"Failed to establish a connection after {self.max_retries} attempts")

# Example usage
if __name__ == "_main_":
    logging.basicConfig(level=logging.INFO)  # Configure logging level
    try:
        db_connection = DatabaseConnection('https://ows.rasdaman.org/rasdaman/ows')
    except ConnectionError as e:
        print("Error occurred:", e)
