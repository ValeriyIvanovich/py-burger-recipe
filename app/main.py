from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: "BurgerRecipe", name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: "BurgerRecipe", objtype: None = None) -> int | str:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: "BurgerRecipe", value: str | int) -> None:
        setattr(obj, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: str | int) -> int | str:
        pass


class Number(Validator):
    def __init__(
            self,
            min_value: int,
            max_value: int
    ) -> None:

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: str | int) -> int | str:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif not self.min_value <= value <= self.max_value:
            raise ValueError(f"Quantity should not be less\
             than {self.min_value} \
            and greater than {self.max_value}.")
        else:
            return value


class OneOf(Validator):
    def __init__(
            self,
            options: tuple
    ) -> None:

        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        else:
            return value


class BurgerRecipe:
    sauce = OneOf(("ketchup", "mayo", "burger"))
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)

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
