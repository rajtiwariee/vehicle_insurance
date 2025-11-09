import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.utils.logger import get_logger
from src.utils.exception import MyException
from src.core.config import settings
from src.configuration.mongo_db_connection import MongoDBClient
logger = get_logger(__name__)


class Proj1Data:
    """
    This class is responsible for fetching mongodb data and exporting it as pandas dataframe
    """
    
    def __init__(self):
        try:
            self.mongodb_client = MongoDBClient(database_name=settings.database_name)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str,database_name: Optional[str] = None) -> pd.DataFrame:
        """_summary_

        Args:
            collection_name (str): The name of the mongodb collection to export
            database_name (Optional[str], optional): Name of the database. Defaults to None.

        Raises:
            MyException: _description_

        Returns:
            pd.DataFrame: _description_
        """
        try:
            #access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongodb_client.database[collection_name]
            else:
                collection = self.mongodb_client[database_name][collection_name]
            
            logger.info(f"Exporting collection {collection_name} as dataframe")
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise MyException(e, sys)



