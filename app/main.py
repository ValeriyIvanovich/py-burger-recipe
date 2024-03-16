from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, obj: str, objtype: None = None) -> None:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: str, value: int) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than"
                             f" {self.min_value} and greater"
                             f" than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, *options: None) -> None:
        self.options = options

    def validate(self, value: int) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(
            self,
            buns: str,
            cheese: str,
            tomatoes: str,
            cutlets: str,
            eggs: str,
            sauce: str
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
