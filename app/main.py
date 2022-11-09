from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance, owner) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value) -> None:
        setattr(instance, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> int:
        if not type(value) is int:
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less"
                             f" than {self.min_value} and greater"
                             f" than {self.max_value}.")
        print(value)
        return value


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be"
                             f" one of ('ketchup', 'mayo', 'burger').")
        print(value)
        return value


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(self, buns: int, cheese: int, tomatoes: int,
                 cutlets: int, eggs: int, sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
