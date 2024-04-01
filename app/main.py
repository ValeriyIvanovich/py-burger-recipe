from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    def __set_name__(self, inst: BurgerRecipe, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, inst: BurgerRecipe, inst_type: Any = None) -> int:
        return getattr(inst, self.protected_name)

    def __set__(self, inst: BurgerRecipe, value: Any) -> None:
        self.validate(value)
        setattr(inst, self.protected_name, value)

    @abstractmethod
    def validate() -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self) -> None:
        self.options = ("ketchup", "mayo", "burger")

    def validate(self, value: Any) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} "
                             f"to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf()

    def __init__(
            self,
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
