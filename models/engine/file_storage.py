#!/usr/bin/python3
"""
FileStorage class for AirBnB clone.
"""
import json
from os import path


class FileStorage:
    """Serializes instances to a JSON file and deserializes them back."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of objects."""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        if not hasattr(obj, "id") or not hasattr(obj, "__class__"):
            raise TypeError("Object must have `id`, `__class__` attributes.")
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self, *args):
        """Serializes __objects to the JSON file."""
        if len(args) > 0:
            raise TypeError("save() takes 1 positional argument but 2 were given")
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        if path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                from models.base_model import BaseModel
                from models.user import User
                from models.amenity import Amenity
                from models.city import City
                from models.place import Place
                from models.review import Review
                from models.state import State

                classes = {
                    "BaseModel": BaseModel,
                    "User": User,
                    "Amenity": Amenity,
                    "City": City,
                    "Place": Place,
                    "Review": Review,
                    "State": State,
                }

                # Deserialize objects
                for key, value in obj_dict.items():
                    class_name = value["__class__"]
                    if class_name in classes:
                        self.__objects[key] = classes[class_name](**value)
                    else:
                        # Handle unexpected or dynamic attributes
                        obj = BaseModel(**value)
                        obj.__dict__.update(value)
                        self.__objects[key] = obj
