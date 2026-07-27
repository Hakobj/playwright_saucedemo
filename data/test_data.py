from data.models import User, Product

# Named users — the app gives us several with different behaviors. Name them once.
STANDARD_USER   = User("standard_user", "secret_sauce")
LOCKED_OUT_USER = User("locked_out_user", "secret_sauce")
PROBLEM_USER    = User("problem_user", "secret_sauce")

# Products with their expected prices — now price is data, not a magic string in an assert.
BACKPACK   = Product("Sauce Labs Backpack", "$29.99")
BIKE_LIGHT = Product("Sauce Labs Bike Light", "$9.99")
