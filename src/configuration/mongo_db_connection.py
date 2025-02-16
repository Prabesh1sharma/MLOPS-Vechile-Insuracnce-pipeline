import os
import pymongo
import sys
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

#load the certificate authority file to avoid timeout error when connecting to mongodb
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the mongodb database.
    Attributes.
    ---------
    client: MongoClient
        A shared MongoClient instances for the class
    database: Database
        The specific database instance that MongoDBClient connects to.
    Methods:
    ------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name

    """
    client = None # Shared MongoClient instances across all MongoDBClient instances

    def __init__(self, database_name: str =  DATABASE_NAME) -> None:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        try:
            #check if a mongodb client connection has already been established; if not create a new one.
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY) # Retrieve MongoDB url from environment variables
                
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY} is not set.")
                # Establish a new MongoDB client connection
                MongoDBClient.client  = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            
            # Use the shared MongoCLient for this instance
            self.client = MongoDBClient.client
            self.database= self.client[database_name] # Connect to the specific database
            self.database_name = database_name
            logging.info("Mongodb conncection is set up successfully")
        except Exception as e:
            # Raise a custom exception with traceback details if connection fails
            raise MyException(e,sys)
        
        
