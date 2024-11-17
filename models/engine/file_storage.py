# file_storage.py
"""file_storage"""
import os
import models
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        obj_dict = {key: obj.to_dict() for key,
                    obj in FileStorage.__objects.items()}
        with open(self.__file_path, "w", encoding='utf-8') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists."""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding='utf-8') as file:
                obj_data = json.load(file)
                # Handle legacy list format
                if isinstance(obj_data, list):
                    for val in obj_data:
                        class_name = val['__class__']
                        obj = globals()[class_name](**val)
                        key = obj.__class__.__name__ + "." + obj.id
                        FileStorage.__objects[key] = obj
                elif isinstance(obj_data, dict):
                    for key, val in obj_data.items():
                        class_name = val['__class__']
                        obj = globals()[class_name](**val)
                        FileStorage.__objects[key] = obj
