from abc import ABC, abstractmethod
from typing import Union, List


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name: str = name
        self.protected_name: str = "_" + name

    def __get__(self, instance: object, owner: type) -> Union[int, str]:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Union[int, str]) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Union[int, str]) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and not greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: List[str]) -> None:
        self.options: List[str] = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} "
                             f"to be one of {tuple(self.options)}.")


class BurgerRecipe:
    buns: Number = Number(2, 3)
    cheese: Number = Number(0, 2)
    tomatoes: Number = Number(0, 3)
    cutlets: Number = Number(1, 3)
    eggs: Number = Number(0, 2)
    sauce: OneOf = OneOf(["ketchup", "mayo", "burger"])

    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: str) -> None:
        self.buns: int = buns
        self.cheese: int = cheese
        self.tomatoes: int = tomatoes
        self.cutlets: int = cutlets
        self.eggs: int = eggs
        self.sauce: str = sauce
