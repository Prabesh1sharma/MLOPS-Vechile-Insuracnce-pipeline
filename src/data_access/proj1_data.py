import sys
import pandas as pd
import numpy as np
from typing import Optional
from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import MyException
from src.constants import DATABASE_NAME
class Proj1Data:
    """
    A class to export  mongodb record into pandas Dataframe
    """
    def __init__(self) -> None:
        """
        Initalize the Mongodb client connection
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise MyException(e,sys)
    def export_collection_ad_dataframe(self, collection_name:str, database_name: Optional[str]=None) ->pd.DataFrame:
        """
        Export an entire mongobc collection  as a pandas dataframe
        Parameter:
        ----------
        collection_name:str
            The name of mongodb collection to export
        database_name :Optional[str]
            Name of database (optional). Defeault to DATABASE_NAME.
        Returns:
        ----------
        pd.DataFrame
            Dataframe containing the collection data , with "_id", column removed and 'na ' values replaced with with NaN.
        """
        try:
            #Acess specified collection from the default of specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection]
            
            #Convert collection data to Dataframe  and preprocess
            print("Fetching data from the mongodb")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fetechde with len: {len(df)}")
            if "id" in df.columns.to_list():
                df = df.drop(columns=['id'], axis=1)
            df.replace({'na':np.nan}, inplace=True)

            return df
        except Exception as e:
            raise MyException(e,sys)
        