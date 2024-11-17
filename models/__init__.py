#!/usr/bin/python3
""" __init__ method """


from .base_model import BaseModel
from .user import User
from .state import State
from .city import City
from .amenity import Amenity
from .place import Place
from .review import Review
from models.engine.file_storage import FileStorage

class_dict = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}

storage = FileStorage()
storage.reload()
