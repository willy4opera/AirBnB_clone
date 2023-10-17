#!/usr/bin/python3
"""Here, we defined the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    cur_brace = re.search(r"\{(.*?)\}", arg)
    dev_backet = re.search(r"\[(.*?)\]", arg)
    if cur_brace is None:
        if dev_backet is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:dev_backet.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(dev_backet.group())
            return retl
    else:
        lexer = split(arg[:cur_brace.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(cur_brace.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """DHere, we efined the AirBnBClone command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        dev_adj = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        dev_match = re.search(r"\.", arg)
        if dev_match is not None:
            d_agl = [arg[:dev_match.span()[0]], arg[dev_match.span()[1]:]]
            dev_match = re.search(r"\((.*?)\)", d_agl[1])
            if dev_match is not None:
                dev_cmd = [d_agl[1][:dev_match.span()[0]],
                           dev_match.group()[1:-1]]
                if dev_cmd[0] in dev_adj.keys():
                    dev_call = "{} {}".format(d_agl[0], dev_cmd[1])
                    return dev_adj[dev_cmd[0]](dev_call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        d_agl = parse(arg)
        if len(d_agl) == 0:
            print("** class name missing **")
        elif d_agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(d_agl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        d_agl = parse(arg)
        dev_obj_dict = storage.all()
        if len(d_agl) == 0:
            print("** class name missing **")
        elif d_agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(d_agl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(d_agl[0], d_agl[1]) not in dev_obj_dict:
            print("** no instance found **")
        else:
            print(dev_obj_dict["{}.{}".format(d_agl[0], d_agl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        d_agl = parse(arg)
        dev_obj_dict = storage.all()
        if len(d_agl) == 0:
            print("** class name missing **")
        elif d_agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(d_agl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(d_agl[0], d_agl[1]) not in dev_obj_dict.keys():
            print("** no instance found **")
        else:
            del dev_obj_dict["{}.{}".format(d_agl[0], d_agl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        d_agl = parse(arg)
        if len(d_agl) > 0 and d_agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            dev_objl = []
            for dobj in storage.all().values():
                if len(d_agl) > 0 and d_agl[0] == dobj.__class__.__name__:
                    dev_objl.append(dobj.__str__())
                elif len(d_agl) == 0:
                    dev_objl.append(dobj.__str__())
            print(dev_objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        d_agl = parse(arg)
        dev_count = 0
        for dobj in storage.all().values():
            if d_agl[0] == dobj.__class__.__name__:
                dev_count += 1
        print(dev_count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        d_agl = parse(arg)
        dev_obj_dict = storage.all()

        if len(d_agl) == 0:
            print("** class name missing **")
            return False
        if d_agl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(d_agl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(d_agl[0], d_agl[1]) not in dev_obj_dict.keys():
            print("** no instance found **")
            return False
        if len(d_agl) == 2:
            print("** attribute name missing **")
            return False
        if len(d_agl) == 3:
            try:
                type(eval(d_agl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(d_agl) == 4:
            dobj = dev_obj_dict["{}.{}".format(d_agl[0], d_agl[1])]
            if d_agl[2] in dobj.__class__.__dict__.keys():
                valtype = type(dobj.__class__.__dict__[d_agl[2]])
                dobj.__dict__[d_agl[2]] = valtype(d_agl[3])
            else:
                dobj.__dict__[d_agl[2]] = d_agl[3]
        elif type(eval(d_agl[2])) == dict:
            dobj = dev_obj_dict["{}.{}".format(d_agl[0], d_agl[1])]
            for num_k, num_v in eval(d_agl[2]).items():
                if (num_k in dobj.__class__.__dict__.keys() and
                        type(dobj.__class__.__dict__[num_k]) in {str, int,
                                                                 float}):
                    valtype = type(dobj.__class__.__dict__[num_k])
                    dobj.__dict__[num_k] = valtype(num_v)
                else:
                    dobj.__dict__[num_k] = num_v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
