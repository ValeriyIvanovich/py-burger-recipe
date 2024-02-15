from abc import ABC, abstractmethod


class Validator(ABC):
    protected_name: str

    def __set_name__(self, owner, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance, owner) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value: object) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: object) -> None:
        pass


class Number(Validator):
    min_value: int
    max_value: int

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: object) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError("Quantity should not be less than "
                             "{self.min_value} and greater than "
                             "{self.max_value}")


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, value: object) -> None:
        if value not in self.options:
            options_str = str(tuple(self.options))
            raise ValueError(f"Expected {value} to be one of {options_str}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

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
