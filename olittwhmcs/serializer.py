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


def create_user_request_parameters(**kwargs):
    """
    Prepare parameters for the create user request.
    :param kwargs: Keyword arguments with user details.
    :return: payload for the create user request
    :rtype: Dictionary
    """
    parameters = get_default_parameters()
    parameters.update({'action': 'AddClient'})
    for param, value in kwargs.items():
        if param == 'first_name':
            parameters.update({'firstname': value})
        if param == 'last_name':
            parameters.update({'lastname': value})
        if param == 'email':
            parameters.update({'email': value})
        if param == 'country':
            parameters.update({'country': value})
        if param == 'state':
            parameters.update({'state': value})
        if param == 'city':
            parameters.update({'city': value})
        if param == 'postcode':
            parameters.update({'postcode': value})
        if param == 'address':
            parameters.update({'address1': value})
        if param == 'phone':
            parameters.update({'phonenumber': value})
        if param == 'password':
            parameters.update({'password2': value})
    return parameters


def get_product_request_parameters(group_id=None, module=None, product_ids=None):
    """
    Retrieve parameters for the products request.
    :param group_id: (Optional) Integer, id of the group from which to fetch products.
    :param module: (Optional) String, name of the module from which to fetch products.
    :param product_ids: (Optional) Integer array, list of product ids to retrieve.
    :return: payload for the get products request
    :rtype: Dictionary
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


def order_request_parameters(client_id, payment_method, billing_cycle, **kwargs):
    parameters = get_default_parameters()
    parameters.update({
        'action': 'AddOrder',
        'clientid': str(client_id),
        'paymentmethod': payment_method,
        'billingcycle': billing_cycle
    })
    for param, value in kwargs.items():
        if param == 'price':
            parameters.update({'priceoverride': value})
        if param == 'promo_code':
            parameters.update({'promocode': value})
        if param == 'affiliate_id':
            parameters.update({'affid': value})
    return parameters


def order_product_request_parameters(client_id, product_id, payment_method, billing_cycle, **kwargs):
    """
    Retrieve parameters for the product order request.
    :param client_id: Integer, id of the client placing the order.
    :param product_id: Integer, id of the product to order.
    :param payment_method: String, preferred method of paying for the order.
        Eg, paypal, rave, ...
    :param billing_cycle: String, billing cycle. Eg, monthly, annually
    :param kwargs: (Optional) Other parameters to add to the order payload.
        Eg promo_code, affiliate_id, price (override), ...
    :return: payload for the order product request
    :rtype: Dictionary
    """
    parameters = order_request_parameters(client_id, payment_method, billing_cycle, **kwargs)
    parameters.update({'pid': product_id})
    return parameters
