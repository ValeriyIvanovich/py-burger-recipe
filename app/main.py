from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance, owner) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value) -> bool:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> bool:
        if isinstance(value, int):
            if (self.min_value <= value <= self.max_value):
                return True
            text_part_1 = f"Quantity should not be less than {self.min_value}"
            text_part_2 = f" and greater than {self.max_value}."
            raise ValueError(text_part_1 + text_part_2)
        raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value) -> bool:
        if isinstance(value, str):
            if value in self.options:
                return True
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        raise TypeError("Option should be string.")


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
