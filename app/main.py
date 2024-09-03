from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: any, objtype: any = None) -> None:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: any, value: any) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value > self.max_value or value < self.min_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value}"
                f" and greater than {self.max_value}"
            )


class OneOf(Validator):
    def __init__(self, *options) -> None:
        self.options = list(options)

    def validate(self, value: any) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one "
                f"of {self.options[0], self.options[1], self.options[2]}."
            )


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(
            self,
            buns: any,
            cheese: any,
            tomatoes: any,
            cutlets: any,
            eggs: any,
            sauce: any
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
