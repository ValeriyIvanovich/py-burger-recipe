from __future__ import annotations
from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> object:
        return getattr(instance, self.protected_name)

    @abstractmethod
    def __set__(self, instance: object, value: object) -> None:
        pass

    @abstractmethod
    def validate(self, value: object) -> None:
        pass


class Number(Validator, ABC):

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif not self.min_value <= value <= self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater "
                             f"than {self.max_value}."
                             )

    def __set__(self, instance: BurgerRecipe, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)


class OneOf(Validator, ABC):

    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")

    def __set__(self, instance: BurgerRecipe, value: str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)


class BurgerRecipe:

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self, buns: int, cheese: int, tomatoes: int, cutlets: int,
                 eggs: int, sauce: tuple) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
