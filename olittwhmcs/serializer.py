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


def get_client_request_parameters(email=None, client_id=None):
    """
    Prepare parameters for the get client request.
    Args:
      email: (Optional) String email of client to retrieve.
      client_id: (Optional) Integer, id of client to retrieve.
    Returns:
      Dictionary, parameters for the get client details request.
    """
    parameters = get_default_parameters()
    parameters.update({'action': 'GetClientsDetails'})
    if email:
        parameters.update({'email': email})
    if client_id:
        parameters.update({'clientid': client_id})
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


def get_client_product_request_parameters(client_id, product_id=None, service_id=None,
                                          domain=None):
    """
    Retrieve parameters for the client products request.
    :param client_id: Integer, id of the client whose products to fetch.
    :param product_id: Integer, specific product id to obtain the details for.
    :param service_id: Integer, specific service id to obtain the details for.
    :param domain: String, specific domain to obtain the service details for.
    :return: payload for the get products request
    :rtype: Dictionary
    """
    parameters = get_default_parameters()
    parameters.update({
        'action': 'GetClientsProducts',
        'clientid': str(client_id)
    })
    if product_id:
        parameters.update({'pid': product_id})
    if service_id:
        parameters.update({'serviceid': service_id})
    if domain:
        parameters.update({'domain': domain})
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


def order_product_request_parameters(client_id, product_id, payment_method,
                                     billing_cycle, **kwargs):
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
    parameters = order_request_parameters(client_id, payment_method, billing_cycle,
                                          **kwargs)
    parameters.update({'pid': product_id})
    return parameters


def upgrade_product_request_parameters(service_id, payment_method, billing_cycle=None,
                                       package_id=None):
    """Retrieve parameters for the product upgrade request.

    Args:
       service_id (int): ID of the service to update.
       payment_method (str): Preferred method of paying for the upgrade.
           Eg, paypal, rave, ...
       billing_cycle (str): (Optional), new product's billing cycle.
       package_id (int): (Optional), package ID to associate with the service.
    Returns:
        Dictionary: Parameters for the upgrade product request
    """
    parameters = get_default_parameters()
    parameters.update({
        'action': 'UpdateClientProduct',
        'serviceid': service_id,
        'paymentmethod': payment_method
    })
    if billing_cycle:
        parameters.update({'billingcycle': billing_cycle})
    if package_id:
        parameters.update({'pid': package_id})
    return parameters


###########
# SERVICE #
###########

def get_upgrade_product_parameters(service_id, payment_method, upgrade_type,
                                   new_product_id=None, new_billing_cycle=None,
                                   promo_code=None):
    """Retrieve parameters for the upgrade product request."""
    parameters = get_default_parameters()
    parameters.update({
        'action': 'UpgradeProduct',
        'serviceid': service_id,
        'paymentmethod': payment_method,
        'type': upgrade_type
    })
    if new_product_id:
        parameters.update({'newproductid': new_product_id})
    if new_billing_cycle:
        parameters.update({'newproductbillingcycle': new_billing_cycle})
    if promo_code:
        parameters.update({'promocode': promo_code})
    return parameters


###########
# INVOICE #
###########

def prepare_get_invoices_request(client_id, status, order_by, order):
    """Prepare parameters for the get invoices request."""
    parameters = get_default_parameters()
    parameters.update({'action': 'GetInvoices'})
    if client_id:
        parameters.update({'userid': client_id})
    if status:
        parameters.update({'status': status})
    if order_by:
        parameters.update({'orderby': order_by})
    if order:
        parameters.update({'order': order})
    return parameters
