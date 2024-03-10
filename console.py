import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class_dict = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


class ConsoleCommand(cmd.Cmd):
    """ ConsoleCommand class. """
    prompt = '(hbnb) '

    def do_create(self, arg):
        """ Creates a new instance of BaseModel or User """
        if not arg:
            print("** class name missing **")
        elif arg not in class_dict.keys():
            print("** class doesn't exist **")
        else:
            new_instance = class_dictarg
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in models.storage.all():
                print("** no instance found **")
            else:
                print(models.storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in models.storage.all():
                print("** no instance found **")
            else:
                del models.storage.all()[key]
                models.storage.save()

    def do_all(self, arg):
        """Prints all string representation """
        args = arg.split()
        if len(args) > 0 and args[0] not in class_dict.keys():
            print("** class doesn't exist **")
        else:
            for obj in models.storage.all().values():
                if (len(args) > 0 and args[0] == obj.__class__.__name__) \
                        or len(args) == 0:
                    print(obj)

    def do_update(self, arg):
        """Updates an instance based on the class name """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif args[0] + "." + args[1] not in models.storage.all():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            key = args[0] + "." + args[1]
            setattr(models.storage.all()[key], args[2], args[3].strip("\""))
            models.storage.save()

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything."""
        pass

    def default(self, line):
        """Method called on an input line """
        if len(line.split(".")) != 2:
            print("*** Unknown syntax: {}".format(line))
        else:
            cls_name = line.split(".")[0]
            action = line.split(".")[1]
            if action == "all()":
                self.do_all(cls_name)
            elif action == "count()":
                self.do_count(cls_name)
            elif action.split("(")[0] == "show":
                id = action.split("\"")[1]
                self.do_show(cls_name + " " + id)
            elif action.split("(")[0] == "destroy":
                id = action.split("\"")[1]
                self.do_destroy(cls_name + " " + id)
            elif action.split("(")[0] == "update":
                id = action.split("\"")[1]
                if "{" in action:
                    attr_dict = eval(action.split(", ", 1)[1][:-1])
                    for attr_name, attr_value in attr_dict.items():
                        self.do_update(cls_name + " " + id + " " +
                                       attr_name + " " + str(attr_value))
                else:
                    attr_name = action.split("\"")[3]
                    attr_value = action.split("\"")[5]
                    self.do_update(cls_name + " " + id + " " +
                                   attr_name + " " + attr_value)

    def do_count(self, arg):
        """Retrieves the number of instances of a class."""
        count = 0
        for key in models.storage.all():
            if arg in key:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
