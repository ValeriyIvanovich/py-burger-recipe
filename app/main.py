from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self,
                     owner: "BurgerRecipe",
                     name: str) -> None:

        self.name = name
        self.protected_name = "_" + self.name

    def __get__(self,
                instance: "BurgerRecipe",
                owner: "BurgerRecipe") -> int | str:

        return getattr(instance, self.protected_name)

    def __set__(self,
                instance: "BurgerRecipe",
                value: str | int) -> None:

        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> int | str:
        pass


class Number(Validator):

    def __init__(self,
                 min_value: int,
                 max_value: int) -> None:

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less "
                             f"than attribute {self.min_value} and "
                             f"greater than attribute {self.max_value}.")
        return True

    def __get__(self,
                instance: "BurgerRecipe",
                owner: "BurgerRecipe") -> int:

        return super().__get__(instance, owner)

    def __set__(self,
                instance: "BurgerRecipe",
                value: int) -> None:

        if self.validate(value):
            super().__set__(instance, value)


class OneOf(Validator):

    def __init__(self, options: tuple[str, str, str]) -> None:
        self.options = options

    def validate(self, value: str) -> bool:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return True

    def __get__(self,
                instance: "BurgerRecipe",
                owner: "BurgerRecipe") -> str:

        return super().__get__(instance, owner)

    def __set__(self,
                instance: "BurgerRecipe",
                value: str) -> None:

        if self.validate(value):
            super().__set__(instance, value)


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
