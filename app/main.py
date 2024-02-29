from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class NumberValidator(Validator):
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


class OneOfValidator(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: int | str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = NumberValidator(2, 3)
    cheese = NumberValidator(0, 2)
    tomatoes = NumberValidator(0, 3)
    cutlets = NumberValidator(1, 3)
    eggs = NumberValidator(0, 2)
    sauce = OneOfValidator(("ketchup", "mayo", "burger"))

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
