from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: [int, str]) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: [int, str]) -> None:
        pass


class Number(Validator):

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: [int, str]) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less "
                             f"than {self.min_value} and "
                             f"greater than {self.max_value}.")


class OneOf(Validator):

    def __init__(self, options: str) -> None:
        self.options = options

    def validate(self, value: [int, str]) -> None:
        if not (value in self.options):
            raise ValueError(f"Expected {value} to be "
                             f"one of {self.options}.")


class BurgerRecipe:

    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options="('ketchup', 'mayo', 'burger')")

    def __init__(self, buns: [int, str], cheese: [int, str],
                 tomatoes: [int, str], cutlets: [int, str],
                 eggs: [int, str], sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
