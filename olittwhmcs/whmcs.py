"""This module contains the api surface for consuming this package."""

from olittwhmcs.exceptions import WhmcsException
from olittwhmcs.models import Product
from olittwhmcs.network import get_whmcs_response
from olittwhmcs.serializer import get_product_request_parameters, order_product_request_parameters


############
# PRODUCTS #
############

def get_products(currency, group_id=None, module=None, product_ids=None):
    """
    Retrieve products from WHMCS.
    :param currency: String, currency in which to display prices. Eg, kes, usd...
    :param group_id: (Optional) Integer, id of the group from which to fetch products. Omit for all groups.
    :param module: (Optional) String, name of the module from which to fetch products. Omit for all modules.
    :param product_ids: (Optional) Integer array, list of product ids to retrieve.
    :return: products retrieved from whmcs
    :rtype: list
    :raises WhmcsException: If an error occurs.
    """
    parameters = get_product_request_parameters(group_id, module, product_ids)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        products = []
        whmcs_products_wrapper = response_or_error.get('products', {})
        whmcs_products = whmcs_products_wrapper.get('product', [])
        for whmcs_product in whmcs_products:
            product = Product(whmcs_product, currency)
            products.append(product)
        return products
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def order_product(client_id, product_id, payment_method, billing_cycle, **kwargs):
    """
    Retrieve products from WHMCS.
    :param currency: String, currency in which to display prices. Eg, kes, usd...
    :param group_id: (Optional) Integer, id of the group from which to fetch products. Omit for all groups.
    :param module: (Optional) String, name of the module from which to fetch products. Omit for all modules.
    :param product_ids: (Optional) Integer array, list of product ids to retrieve.
    :return: products retrieved from whmcs
    :rtype: list
    :raises WhmcsException: If an error occurs.
    """
    parameters = order_product_request_parameters(client_id, product_id, payment_method, billing_cycle, **kwargs)
    return parameters
    # is_successful, response_or_error = get_whmcs_response(parameters)
    # if is_successful and response_or_error:
    #     products = []
    #     whmcs_products_wrapper = response_or_error.get('products', {})
    #     whmcs_products = whmcs_products_wrapper.get('product', [])
    #     for whmcs_product in whmcs_products:
    #         product = Product(whmcs_product, currency)
    #         products.append(product)
    #     return products
    # default_error = "Unable to fetch products"
    # raise WhmcsException(response_or_error if response_or_error else default_error)

############
# ORDERS #
############
