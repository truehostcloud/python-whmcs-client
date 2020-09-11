"""This module contains the api surface for consuming this package."""

from olittwhmcs import network

from olittwhmcs import serializer
from olittwhmcs.exceptions import WhmcsException
from olittwhmcs.models import Product


def get_products(group_id=None, module=None, product_ids=None):
    """
    Retrieve products from WHMCS.
    :param group_id: (Optional) Integer, id of the group from which to fetch products. Omit for all groups.
    :param module: (Optional) String, name of the module from which to fetch products. Omit for all modules.
    :param product_ids: (Optional) Integer array, list of product ids to retrieve.
    :return: products retrieved from whmcs
    :rtype: list
    :raises WhmcsException: If an error occurs.
    """
    parameters = serializer.get_product_request_parameters(group_id, module, product_ids)
    is_successful, response_or_error = network.get_whmcs_response(parameters)
    if is_successful:
        return response_or_error
        products = []
        for product in response_or_error:
            products.append(Product(product))
            return products
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)
