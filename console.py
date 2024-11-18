#!/usr/bin/python3
"""Console module for AirBnB clone."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""
    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print("")
        return True

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print its ID."""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_reload(self, arg):
        """Reload all objects from the storage file."""
        try:
            storage.reload()
            print("Objects reloaded successfully.")
        except Exception as e:
            print(f"Error during reload: {e}")

    def do_show(self, arg):
        """Show an instance of a class based on class name and ID."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        """Destroy an instance based on class name and ID."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Print all instances or instances of a specific class."""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return
        objs = [
            str(obj) for obj in storage.all().values()
            if not arg or obj.__class__.__name__ == arg
        ]
        print(objs)

    def do_update(self, arg):
        """Update an instance based on class name and ID."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(obj, args[2], eval(args[3]))
        obj.save()

    def default(self, line):
        """Handle commands in <ClassName>.command() format."""
        try:
            class_name, command = line.split(".", 1)
            if class_name not in self.classes:
                print(f"*** Unknown syntax: {line}")
                return

            if command.startswith("update("):
                try:
                    args = command[len("update("):-1].split(", ", maxsplit=2)
                    if len(args) < 3:
                        print("** value missing **")
                        return

                    instance_id = args[0].strip('"')
                    attribute_name = args[1].strip('"')
                    value = args[2].strip('"')

                    # Convert value appropriately
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                        value = float(value)
                    else:
                        value = value.strip('"')

                    key = f"{class_name}.{instance_id}"
                    obj = storage.all().get(key)
                    if not obj:
                        print("** no instance found **")
                        return

                    setattr(obj, attribute_name, value)
                    obj.save()
                except Exception:
                    print("** Invalid arguments **")
                return

            elif command.startswith("show("):
                instance_id = command[len("show("):-1].strip('"')
                key = f"{class_name}.{instance_id}"
                obj = storage.all().get(key)
                if obj:
                    print(obj)
                else:
                    print("** no instance found **")
                return

            elif command.startswith("count()"):
                count = sum(1 for obj in storage.all().values()
                            if obj.__class__.__name__ == class_name)
                print(count)
                return

            elif command.startswith("all()"):
                objs = [str(obj) for obj in storage.all().values()
                        if obj.__class__.__name__ == class_name]
                print(objs)
                return

            print(f"*** Unknown syntax: {line}")
        except ValueError:
            print(f"*** Unknown syntax: {line}")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
