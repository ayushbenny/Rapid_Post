# RapidDB

RapidDB is a Python class for handling database operations using RapidDB.

## Installation

To use RapidDB, you need to have the following dependencies installed:

- psycopg2

You can install the dependencies using pip:

pip install psycopg2


## Usage

To use RapidDB, follow the example below:

```python
from rapiddb import RapidDB

# Define your database credentials
db_credentials = {
    "database": "rapid_db",
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "5432",
}

# Create an instance of RapidDB
rapid_db = RapidDB(db_credentials)

# The database table will be created based on the provided payload in the constructor.
# Data will be inserted into the table automatically.

# Use RapidDB for your database operations
# ...

Class Documentation
RapidDB Class
A class for handling database operations using RapidDB.


Constructor

def __init__(self, db_credentials):
    """
    Initializes a RapidDB object.

    Args:
        db_credentials (dict): A dictionary containing the database connection credentials.

    Attributes:
        db_credentials (dict): The database connection credentials.
        rapid_db_connect (RapidDBConnect): An instance of the RapidDBConnect class for database connection.
    """

Methods

_rapid_db_connect

@property
def _rapid_db_connect(self):
    """
    Creates a connection to the Postgres Database.

    Returns:
        psycopg2.extensions.connection: The database connection object.

    Raises:
        Exception: If an error occurs while connecting to the database.
    """

_rapid_payload_analyzer

def _rapid_payload_analyzer(self):
    """
    Analyzes the payload and extracts the data to create the database table.

    Returns:
        str: The create table query generated from the payload.

    Note:
        The payload should be a dictionary where the keys represent the column names
        and the values represent the corresponding data types.

    Raises:
        None.
    """

_rapid_db_create

def _rapid_db_create(self, query):
    """
    Executes the query to create the database table based on the payload data.

    Args:
        query (str): The SQL query to create the table.

    Returns:
        None

    Raises:
        None
    """

_rapid_db_insert

def _rapid_db_insert(self):
    """
    Inserts data into the table that has been created in the `_rapid_db_create` function.

    Returns:
        None

    Raises:
        None
    """
