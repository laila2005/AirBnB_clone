#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
import models  # Import models module directly to avoid circular import issues


class BaseModel:
    """Defines common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Updates `updated_at` and saves instance to storage."""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance."""
        dict_repr = self.__dict__.copy()
        dict_repr["__class__"] = self.__class__.__name__
        dict_repr["created_at"] = self.created_at.isoformat()
        dict_repr["updated_at"] = self.updated_at.isoformat()
        return dict_repr

    def __str__(self):
        """Returns string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"