from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.protected_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.protected_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if self.min_value is not None:
            if value < self.min_value or value > self.max_value:
                raise ValueError(
                    f"Quantity should not be less than {self.min_value} and "
                    f"greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, *options):
        self.options = tuple(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value} to be "
                             f"one of {self.options}.")


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(self, buns, cheese, tomatoes, cutlets, eggs, sauce):
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
