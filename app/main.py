from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, name: str) -> None:
        self.protected_name = "_" + name

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass


class Number(Validator):
    def __init__(self, name: str, min_value: int, max_value: int) -> None:
        super().__init__(name)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"Quantity should not be less than"
                f" {self.min_value} and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, name: str, *options: str) -> None:
        super().__init__(name)
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number("buns", 2, 3)
    cheese = Number("cheese", 0, 2)
    tomatoes = Number("tomatoes", 0, 3)
    cutlets = Number("cutlets", 1, 3)
    eggs = Number("eggs", 0, 2)
    sauce = OneOf("sauce", "ketchup", "mayo", "burger")

    def __init__(self, buns: str, cheese: str, tomatoes: str, cutlets: str,
                 eggs: str, sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
