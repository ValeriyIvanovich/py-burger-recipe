from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int | str) -> None:
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator, ABC):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set__(self, instance: object, value: int | str) -> None:
        setattr(instance, self.protected_name, self.validate(value))

    def validate(self, value: int | str) -> int | str:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if self.min_value > value or self.max_value < value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than"
                             f" {self.max_value}.")
        return value


class OneOf(Validator, ABC):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def __set__(self, instance: object, option: int | str) -> None:
        setattr(instance, self.protected_name, self.validate(option))

    def validate(self, value: int | str) -> int | str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return value


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
                 sauce: str
                 ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self. cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
