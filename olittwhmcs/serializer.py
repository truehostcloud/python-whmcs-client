"""This module contains functions for processing whmcs request payloads."""

import os


def get_default_parameters():
    """Retrieve parameters required for all whmcs requests."""
    return {
        'identifier': os.environ.get('WHMCS_IDENTIFIER_KEY', ''),
        'secret': os.environ.get('WHMCS_SECRET_KEY', ''),
        'accesskey': os.environ.get('WHMCS_ACCESS_KEY', ''),
        'responsetype': 'json'
    }


def get_product_request_parameters(group_id=None, module=None, product_ids=None):
    """
    Retrieve parameters for the products request.
    :param group_id: (Optional) Integer, id of the group from which to fetch products.
    :param module: (Optional) String, name of the module from which to fetch products.
    :param product_ids: (Optional) Integer array, list of product ids to retrieve.
    """
    parameters = get_default_parameters()
    parameters.update({'action': 'GetProducts'})
    if group_id:
        parameters.update({'gid': group_id})
    if module:
        parameters.update({'module': module})
    if product_ids:
        parameters.update({'pid': ','.join(map(str, product_ids))})
    return parameters
