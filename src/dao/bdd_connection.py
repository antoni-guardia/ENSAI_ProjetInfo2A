import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
import logging
from utils.singleton import Singleton

# Setup logging to a file
logging.basicConfig(
    filename="db_connection_errors.log",  # Log file to store errors
    level=logging.ERROR,  # Set log level to ERROR to capture only error-level logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    Handles PostgreSQL database connection with error suppression and logging.
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)

        # Check if required environment variables are set
        required_env_vars = [
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_DATABASE",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_SCHEMA",
        ]

        for var in required_env_vars:
            if var not in os.environ:
                self._log_error(f"Environment variable {var} is not set.")
                return  # Skip if any variable is missing

        # Open the connection and handle errors silently
        try:
            self.__connection = psycopg2.connect(
                host=os.environ["POSTGRES_HOST"],
                port=os.environ["POSTGRES_PORT"],
                database=os.environ["POSTGRES_DATABASE"],
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                options=f"-c search_path={os.environ['POSTGRES_SCHEMA']}",
                cursor_factory=RealDictCursor,
            )
        except OperationalError as e:
            self._log_error(f"Failed to connect to the database: {e}")
            self.__connection = None  # Set connection to None on failure

    @property
    def connection(self):
        """
        Return the opened connection or None if the connection failed.

        :return: the opened connection or None.
        """
        if not self.__connection:
            self._log_error("No active database connection.")
        return self.__connection

    def close(self):
        """Close the connection when done."""
        if self.__connection:
            try:
                self.__connection.close()
            except Exception as e:
                self._log_error(f"Error closing the connection: {e}")

    def _log_error(self, message):
        """
        Logs errors to the 'db_connection_errors.log' file.

        :param message: The error message to log.
        """
        logging.error(message)
        # Optionally, you can raise exceptions here if you want them to be re-raised
        # raise Exception(message)  # Uncomment to raise the exception if necessary
