"""
OLITT WHMCS
"""

from olittwhmcs import network

from olittwhmcs import request_parameters
from olittwhmcs.models import Product


def get_products(url, group_id=None, module=None, product_ids=None):
    """
    Retrieve products from WHMCS.
    :group_id: Integer, id of the group from which to fetch products. Omit for all groups.
    :module_name: (Optional) String, name of the module from which to fetch products. Omit for all modules.
    :product_ids: (Optional) Integer array, list of product ids to retrieve.
    """
    url = "https://www.olitt.com/billing/includes/api.php"
    parameters = request_parameters.get_product_request_parameters(group_id, module, product_ids)
    is_successful, products_response = network.get_whmcs_response(url, parameters)

    print(products_response)

    products = []
    for product in products_response:
        products.append(Product(product))

    return products
