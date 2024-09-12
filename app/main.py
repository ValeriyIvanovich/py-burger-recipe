from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    def __set_name__(self, owner: BurgerRecipe, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: BurgerRecipe, owner: BurgerRecipe) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: BurgerRecipe, value: str | int) -> None:
        return setattr(instance, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> int:
        super().validate(value)
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif self.min_value <= value <= self.max_value:
            return value
        else:
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: list = None) -> None:
        self.options = \
            ("ketchup", "mayo", "burger") if not options else options

    def validate(self, value: Any) -> str:
        super().validate(value)
        if value in self.options:
            return value
        else:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf()

    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: str
                 ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce

    def add_buns(self, value: int) -> None:
        self.buns = value

    def add_cheese(self, value: int) -> None:
        self.cheese = value

    def add_tomatoes(self, value: int) -> None:
        self.tomatoes = value

    def add_cutlets(self, value: int) -> None:
        self.cutlets = value

    def add_eggs(self, value: int) -> None:
        self.eggs = value

    def add_sauce(self, value: int) -> None:
        self.sauce = value
