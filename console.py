#!/usr/bin/python3

"""An interactive shell?"""

import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""

    prompt = '(hbnb) '

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
