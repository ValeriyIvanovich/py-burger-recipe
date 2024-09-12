from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: str, owner: str) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: str, value: str) -> None:
        setattr(instance, self.protected_name, value)
        self.validate(value)

    @abstractmethod
    def validate(self, value: str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: str) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value not in range(self.min_value, self.max_value + 1):
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than {self.max_value}"
            )


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {tuple(self.options)}."
            )
        else:
            print("burger will be created")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

    def __init__(self, buns: str,
                 cheese: str,
                 tomatoes: str,
                 cutlets: str,
                 eggs: str,
                 sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
