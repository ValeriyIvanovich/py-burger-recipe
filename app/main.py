from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value) -> None:
        pass


class Number(Validator):

    def __init__(self,
                 min_value: int = None,
                 max_value: int = None) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less"
                             f"than {self.min_value} and"
                             f"greater than {self.max_value}.")
        return True


class OneOf(Validator):

    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be "
                             f"one of {self.options}.")


class BurgerRecipe:

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
