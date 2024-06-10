from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: str, owner: str) -> int:
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance: str, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"{self.public_name.capitalize()} should be an integer."
            )


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if (value < self.min_value
                or value > self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of ({self.options})."
            )


class BurgerRecipe:
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

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("'ketchup', 'mayo', 'burger'")
