from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.config import settings

class MongoDBConnector:
    _instance: MongoClient | None = None
    
    def __new__(cls, *args, **kwargs) -> MongoClient:
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.DATABASE_HOST)
            except ConnectionFailure as cf:
                raise ConnectionFailure(f"Failed to connect to database: {cf}")
            
        print("Connection to Database Successful")
        
        return cls._instance
    
    def close(self):
        if self._instance:
            self._instance.close()
            print("Connection to database closed")
            
connection = MongoDBConnector()
        
        