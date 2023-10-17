#!/usr/bin/python3
"""Here, we defined the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        dec_ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(dec_ocname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        dev_odict = FileStorage.__objects
        dev_obdic = {obj: dev_odict[obj].to_dict() for obj in dev_odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(dev_obdic, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                dev_obdic = json.load(f)
                for num in dev_obdic.values():
                    dev_cls_name = num["__class__"]
                    del num["__class__"]
                    self.new(eval(dev_cls_name)(**num))
        except FileNotFoundError:
            return
