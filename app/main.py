from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: any, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: "BurgerRecipe", owner: any) -> any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: "BurgerRecipe", value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

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
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: int) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of "
                             f"{self.options}.")


class BurgerRecipe:
    buns: Number = Number(min_value=2, max_value=3)
    cheese: Number = Number(min_value=0, max_value=2)
    tomatoes: Number = Number(min_value=0, max_value=3)
    cutlets: Number = Number(min_value=1, max_value=3)
    eggs: Number = Number(min_value=0, max_value=2)
    sauce: OneOf = OneOf(options=("ketchup", "mayo", "burger"))

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
