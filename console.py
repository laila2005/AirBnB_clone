#!/usr/bin/python3
import cmd
from models import storage, class_dict
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict:
            print("** class doesn't exist **")
        else:
            new_instance = class_dict[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass

    def do_help(self, arg):
        """Help command"""
        super().do_help(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
