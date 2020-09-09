"""
OLITT WHMCS
"""

from whmcs.olittwhmcs import api

from whmcs.olittwhmcs import request_parameters


def get_products(group_id=None, module=None, product_ids=None):
    """
    Retrieve products from WHMCS.
    :group_id: Integer, id of the group from which to fetch products. Omit for all groups.
    :module_name: (Optional) String, name of the module from which to fetch products. Omit for all modules.
    :product_ids: (Optional) Integer array, list of product ids to retrieve.
    """
    url = "https://www.olitt.com/billing/includes/api.php"
    parameters = request_parameters.get_product_request_parameters(group_id, module, product_ids)
    is_successful, products_response = api.get_whmcs_response(url, parameters)
    print(products_response)
    return products_response
