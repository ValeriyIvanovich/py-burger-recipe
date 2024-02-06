from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: tuple, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: type, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: type, value: int | str) -> None:
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be "
                             f"less than {self.min_value} and "
                             f"greater than {self.max_value}.")
        return value


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> str:
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

    def __init__(self, buns: int, cheese: int, tomatoes: int,
                 cutlets: int, eggs: int, sauce: str) -> None:
        self.buns = Number(2, 3).validate(buns)
        self.cheese = Number(0, 2).validate(cheese)
        self.tomatoes = Number(0, 3).validate(tomatoes)
        self.cutlets = Number(1, 3).validate(cutlets)
        self.eggs = Number(0, 2).validate(eggs)
        self.sauce = OneOf(("ketchup", "mayo", "burger")).validate(sauce)
