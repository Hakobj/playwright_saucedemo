# shopping_list = []          # module-level = SHARED across tests. This is the bug.

def test_adds_two_items():
    shopping_list = []
    shopping_list.append("backpack")
    shopping_list.append("bike-light")
    assert len(shopping_list) == 2

def test_starts_empty():
    shopping_list = []
    assert len(shopping_list) == 0   # assumes nothing else touched the list
