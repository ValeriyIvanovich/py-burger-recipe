from __future__ import annotations

from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: callable, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass

    def __get__(self, instance: callable, owner: callable) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: callable, value: int | str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)


class Number(Validator):
    def __init__(
            self,
            min_value: int,
            max_value: int
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int | str) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        else:
            if not (self.min_value <= value <= self.max_value):
                raise ValueError(
                    f"Quantity should not be less than {self.min_value} "
                    f"and greater than {self.max_value}."
                )


class OneOf(Validator):

    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: int | str) -> None:
        if not (value in self.options):
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))
    print("burger will be created")

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
