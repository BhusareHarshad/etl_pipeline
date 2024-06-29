import uuid
from typing import List, Optional

from utils.config import settings
from database.mongodb import connection
from utils.errors import ImproperlyConfigured
from pydantic import UUID4, BaseModel, ConfigDict, Field
from pymongo import errors

_database = connection.get_database(settings.DATABASE_NAME)

class BaseDocument(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    def to_mongo(self, **kwargs) -> dict:
        """Convert "id" (UUID object) into "_id" (str object)."""
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(
            exclude_unset=exclude_unset, by_alias=by_alias, **kwargs
        )

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))

        return parsed

    def save(self, **kwargs):
        collection = _database[self._get_collection_name()]
        try:
            result = collection.insert_one(self.to_mongo(**kwargs))
            return result.inserted_id
        except errors.WriteError as e:
            return None
        
    def _get_collection_name(cls):
        if not hasattr(cls, "Settings") or not hasattr(cls.Settings, "name"):
            raise ImproperlyConfigured(
                "Document should define an Settings configuration class with the name of the collection."
            )
        return cls.Settings.name
        
        
class RepositoryDocument(BaseDocument):
    name: str
    link: str
    content: dict
    #owner_id: str = Field(alias="owner_id")

    class Settings:
        name = "repositories"