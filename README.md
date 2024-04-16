# Burger Recipe

**Please note:** read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md)
before starting.

You work at the **In-N-Out** and make delicious burgers. 

Create the `BurgerRecipe` class. Its `__init__` method should accept and save the number of ingredients needed to make a burger, such as cheese, tomatoes, cutlets, eggs, buns, and sauce.

```python
cheese_burger = Burger(buns=2, cheese=2, tomatoes=1, cutlets=1, eggs=1, sauce="ketchup")
```

You can make burgers with a different number of ingredients and different sauces, for example:

- `buns` — can range from `2` to `3`;
- `cheese` — can range from `0` to `2`;
- `tomatoes` — can range from `0` to `3`;
- `cutlets` — can range from `1` to `3`;
- `eggs` — can range from `0` to `2`;
- `sauce` — can be `ketchup`, `mayo`, or `burger`.

So, it would be convenient to use descriptors to ensure that the number of ingredients is `int` in a range mentioned above 
and the sauce is one of `ketchup`, `mayo`, or `burger`.

The main task is to create the `BurgerRecipe` class, and for convenience, you should consider the descriptors.

Implement the `Validator` class that will have such methods:

- the `__set_name__` method, which accepts the name of the attribute, adds `_` to its beginning, and stores it in the `protected_name` attribute;
- the `__get__` method that returns the attribute value;
- the `__set__` method, which sets the attribute value (**note** that there should be no validation implemented, you should only call it there);
- the `validate` abstract method, which accepts the `value`.

Also, you need to implement the `Number` class, which is the `Validator` child class. It should have:

- the `__init__` method, which accepts and stores the `min_value` and the `max_value`;
- the `validate` method, which checks the value type, and if the type is incorrect, it must raise the `TypeError` exception with the `Quantity should be integer.` message.
Then it should check whether the value is within `min_value` and `max_value`. If it’s not, it should raise the `ValueError` with the `Quantity should not be less than {self.min_value} and greater than {self.max_value}.` message.

Last but not least, you need to implement the `OneOf` validator, which is the child class of the `Validator` class. It allows to choose one of the provided values and should have:
- the `__init__` method, which accepts and stores `options`;
- the `validate` method, which accepts the `value` and checks if it’s one of the provided options and, if not — raises the `ValueError` with the `Expected {value} to be one of {self.options}.` message.

```python
burger = BurgerRecipe(buns="1", cheese="1", tomatoes="1", cutlets="1", eggs="1", sauce="mayo")
 # TypeError: Quantity should be integer.

burger = BurgerRecipe(buns=1, cheese=10, tomatoes=1, cutlets=1, eggs=1, sauce="mayo")
 # ValueError: Quantity should not be less than 2 and greater than 3.

burger = BurgerRecipe(buns=2, cheese=1, tomatoes=1, cutlets=1, eggs=1, sauce="mustard") 
# ValueError: Expected mustard to be one of ('ketchup', 'mayo', 'burger').

burger = BurgerRecipe(buns=2, cheese=1, tomatoes=1, cutlets=1, eggs=1, sauce="ketchup")
# burger will be created
```

**Please note:** descriptors should be created as class attributes.
