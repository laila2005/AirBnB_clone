#!/usr/bin/python3
"""Console module."""

import cmd
import json
from models import storage, class_dict
from models.base_model import BaseModel
import models


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class."""
    prompt = '(hbnb)  '

    def do_create(self, arg):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file), and prints the id."""
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
        """Prints the string representation of an instance
        based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
        based or not on the class name."""
        args = arg.split()
        if len(args) > 0 and args[0] not in class_dict:
            print("** class doesn't exist **")
        else:
            for obj in storage.all().values():
                if len(args) == 0 or obj.__class__.__name__ == args[0]:
                    print(obj)

    def default(self, line):
        """Called on an input line when
        the command prefix is not recognized."""
        if '.' in line:
            args = line.split('.')
            class_name = args[0]
            command = args[1].split('(')[0]
            if class_name not in class_dict:
                print("** class doesn't exist **")
            elif command not in ["show", "destroy", "update", "all", "count"]:
                print("** command doesn't exist **")
            else:
                try:
                    id = args[1].split('(')[1].split(')')[0]
                    if id == "":
                        print("** instance id missing **")
                    else:
                        if command == "show":
                            self.do_show(class_name + " " + id)
                        elif command == "destroy":
                            self.do_destroy(class_name + " " + id)
                        elif command == "update":
                            id, attr_dict = command.split('"')[1], \
                                            command.split('{')[1][:-1]
                            if ':' in attr_dict:
                                attr_dict = json.loads('{' + attr_dict + '}')
                                for key, value in attr_dict.items():
                                    self.do_update(f"{class_name} {id} {key} "
                                                   f"{str(value)}")
                            else:
                                attr_name, attr_value = attr_dict.split(", ")
                                self.do_update(f"{class_name} {id} {attr_name}"
                                               f"{attr_value}")
                        elif command == "all":
                            self.do_all(class_name)
                        elif command == "count":
                            self.do_count(class_name)
                except IndexError:
                    print("** no instance found **")
        else:
            print("*** Unknown syntax: " + line)

    def do_count(self, arg):
        """Counts the number of instances of a class."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict:
            print("** class doesn't exist **")
        else:
            count = 0
            for key in storage.all():
                if key.split('.')[0] == args[0]:
                    count += 1
            print(count)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            else:
                try:
                    value = float(args[3]) if '.' in args[3] else int(args[3])
                except ValueError:
                    value = args[3]
                setattr(storage.all()[key], args[2], value)
                storage.save()

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn't execute anything."""
        pass

    def do_help(self, arg):
        """Help command."""
        super().do_help(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
