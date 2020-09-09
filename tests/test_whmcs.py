from olittwhmcs import whmcs


def test_get_products():
    retrieved_products = whmcs.get_products()
    assert type(retrieved_products) == (dict or list)
    # assert retrieved_products == ""
