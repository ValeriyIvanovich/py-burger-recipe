class Validator:
    def __set_name__(self, name):
        self.name = name
        self.protected_name = f"_{name}"
    
    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)
    
    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.protected_name, value)



class Number(Validator):
    def __init__(self, min_vlaue: int, max_value: int) -> None:
        self.min_value = min_vlaue
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise TypeError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}.")
        



class OneOf(Validator):
    pass


class BurgerRecipe:
    def __init__(self) -> None:
        pass