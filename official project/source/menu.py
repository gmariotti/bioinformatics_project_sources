from __future__ import print_function

import logging

from singleton import Singleton


class Menu(object):
    __metaclass__ = Singleton

    def __init__(self, title, indicator="[Select Option] >>> "):
        self.title = title
        self.options = []
        self.indicator = indicator

    def add_options(self, *options):
        for option in options:
            if isinstance(option, Option):
                self.options.append(option)
            else:
                message = "{0} is not an Option".format(option)
                logging.error(message)

    def reset_options(self):
        self.options = []

    def select_option(self):
        try:
            option = int(input(self.indicator)) - 1
            if self.validate(option):
                self.options[option]()
        except ValueError as ve:
            logging.error(ve.message)

    def validate(self, option):
        if -1 < option < len(self.options):
            return True
        raise ValueError("{0} is not a valid option".format(option))

    def show(self):
        print(self.title, end="\n\n")
        for (key, option) in enumerate(self.options):
            num = key + 1
            print("({0})\t{1}".format(num, option))


class Option(object):
    """
    Represent an Option in the menu, with its name and a comment of what it
    can do, and a callable object in order to perform the corresponding job.
    """

    def __init__(self, name, comment, callable_obj):
        if callable(callable_obj):
            self.callable = callable_obj
            self.name = name
            self.comment = comment
        else:
            message = "{0} is not callable_obj".format(callable_obj)
            logging.error(message)
            raise SyntaxError(message)

    def __call__(self, *args, **kwargs):
        self.callable(*args, **kwargs)

    def __str__(self):
        return "{0}\n\t{1}\n".format(self.name, self.comment)
