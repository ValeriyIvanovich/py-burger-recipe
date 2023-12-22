from __future__ import annotations

from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self,
                     owner: type,
                     name: str,
                     ) -> None:
        self.protected_name = f"_{name}"

    def __get__(self,
                obj: BurgerRecipe,
                obj_type: type,
                ):
        return getattr(obj, self.protected_name)

    def __set__(self,
                obj: BurgerRecipe,
                value: int | str,
                ) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        """ abstract method, which accepts the value """


class Number(Validator):

    def __init__(self,
                 min_value: int,
                 max_value: int,
                 ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Quantity should not be less "
                             f"than {self.min_value} and "
                             f"greater than {self.max_value}")


class OneOf(Validator):

    def __init__(self, options: tuple[str]) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be "
                             f"one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(('ketchup', 'mayo', 'burger'))

    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: list[str],
                 ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
