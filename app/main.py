from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner: object, name: str) -> None:
        print("__set_name__")
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> object:
        print("__get__")
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int | str) -> None:
        print("__set__")
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self) -> None:
        pass


class Number(Validator):

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Quantity should not be "
                             f"less than {self.min_value} "
                             f"and greater than {self.max_value}.")
        return value


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> object:
        if value in self.options:
            return value
        raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options=("ketchup", "mayo", "burger"))

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
