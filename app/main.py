from abc import ABC, abstractmethod
from typing import Tuple


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: object) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: object) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than {self.max_value}"
            )


class OneOf(Validator):
    def __init__(self, options: Tuple[str, ...]) -> None:
        self.options = options

    def validate(self, value: object) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns: Number = Number(2, 3)
    cheese: Number = Number(0, 2)
    tomatoes: Number = Number(0, 3)
    cutlets: Number = Number(1, 3)
    eggs: Number = Number(0, 2)
    sauce: OneOf = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(
        self,
        buns: Number,
        cheese: Number,
        tomatoes: Number,
        cutlets: Number,
        eggs: Number,
        sauce: OneOf,
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
