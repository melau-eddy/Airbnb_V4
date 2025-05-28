#!/usr/bin/python3
"""Console module for HBNB project"""

import cmd
import shlex
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity, "BaseModel": BaseModel, "City": City,
    "Place": Place, "Review": Review, "State": State, "User": User
}


class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter"""
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exit console on EOF"""
        return True

    def emptyline(self):
        """Do nothing on empty line"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """Parse key-value pairs from arguments"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Create new class instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        
        new_dict = self._key_value_parser(args[1:])
        instance = classes[args[0]](**new_dict)
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Print instance string representation"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = f"{args[0]}.{args[1]}"
        all_objs = models.storage.all()
        print(all_objs.get(key, "** no instance found **"))

    def do_destroy(self, arg):
        """Delete instance by class name and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = f"{args[0]}.{args[1]}"
        all_objs = models.storage.all()
        if key in all_objs:
            del all_objs[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Print all instances or instances of specific class"""
        args = shlex.split(arg)
        if not args:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return
            
        obj_list = [str(obj) for obj in obj_dict.values()]
        print(f"[{', '.join(obj_list)}]")

    def do_update(self, arg):
        """Update instance attribute"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
            
        key = f"{args[0]}.{args[1]}"
        all_objs = models.storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
            
        obj = all_objs[key]
        value = args[3]
        
        # Special handling for Place class attributes
        if args[0] == "Place":
            numeric_attrs = {
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "price_by_night": int,
                "latitude": float,
                "longitude": float
            }
            if args[2] in numeric_attrs:
                try:
                    value = numeric_attrs[args[2]](value)
                except ValueError:
                    value = 0 if numeric_attrs[args[2]] == int else 0.0
        
        setattr(obj, args[2], value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()