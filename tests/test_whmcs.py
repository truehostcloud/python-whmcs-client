from olittwhmcs import api


def test_get_products():
    retrieved_products = api.get_products()
    # assert type(retrieved_products) == (dict or list)
    # assert retrieved_products == ""
