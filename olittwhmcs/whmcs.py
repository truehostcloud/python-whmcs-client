"""This module contains the api surface for consuming this package."""

import hashlib
import time
from datetime import datetime
from olittwhmcs.exceptions import WhmcsException
from olittwhmcs.models import Product
from olittwhmcs.network import get_whmcs_response
from olittwhmcs.serializer import get_product_request_parameters, order_product_request_parameters, \
    create_user_request_parameters, get_user_product_request_parameters


############
# ACCOUNTS #
############

def create_client(**kwargs):
    """
    Create a WHMCS User account.
    :param kwargs: Keyword arguments with user details.
        first_name, last_name, email, country, state, city,
        postcode, address, phone, password
    :return: products retrieved from whmcs
    :rtype: list
    :raises WhmcsException: If an error occurs.
    """
    parameters = create_user_request_parameters(**kwargs)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        client_id = response_or_error.get('clientid')
        return client_id
    default_error = "Unable to enroll for a billing account"
    raise WhmcsException(response_or_error if response_or_error else default_error)


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


def get_client_products(client_id, ):
    """
    Retrieve a user's products from WHMCS.
    :param user_id: Integer, id of the user whose products to fetch.
    """
    parameters = get_user_product_request_parameters(group_id, module, product_ids)


def order_product(client_id, product_id, payment_method, billing_cycle, **kwargs):
    """
    Place a product order in WHMCS.
    :param client_id: Integer, id of the client placing the order.
    :param product_id: Integer, id of the product to order.
    :param payment_method: String, preferred method of paying for the order.
        Eg, paypal, rave, ...
    :param billing_cycle: String, billing cycle. Eg, monthly, annually
    :param kwargs: (Optional) Other parameters to add to the order payload.
        Eg promo_code, affiliate_id, price (override), ...
    :return: id of placed order, id of corresponding invoice
    :rtype: int, int
    :raises WhmcsException: If an error occurs.
    """
    parameters = order_product_request_parameters(client_id, product_id, payment_method, billing_cycle, **kwargs)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        order_id = response_or_error.get('orderid')
        invoice_id = response_or_error.get('invoiceid')
        return order_id, invoice_id
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


############
# INVOICES #
############

def get_settle_invoice_url(invoice_id, client_email, auto_auth_key):
    """
    Generate a url to preview and pay for the invoice.
    :param invoice_id: Integer, id of the invoice to pay.
    :param client_email: String, email of the whmcs user.
    :param auto_auth_key: String, key to autologin the user.
    :return: A url to pay for an invoice.
    :rtype: String.
    """

    def get_timestamp():
        timestamp_float = time.mktime(datetime.now().timetuple())
        timestamp_int = int(timestamp_float)
        timestamp_string = str(timestamp_int)
        return timestamp_string

    def generate_whmcs_hash(email):
        concatenated_string = '{}{}{}'.format(email, get_timestamp(), auto_auth_key)
        hash_object = hashlib.sha1(concatenated_string.encode())
        pb_hash = hash_object.hexdigest()
        return pb_hash

    whmcs_hash = generate_whmcs_hash(client_email)

    base_url = 'https://www.olitt.com/billing'

    invoice_url = '{}{}?id={}'.format(base_url, '/viewinvoice.php', invoice_id)
    parameters = 'email={}&timestamp={}&hash={}&goto={}'.format(client_email, get_timestamp(), whmcs_hash, invoice_url)
    payment_url = '{}{}?{}'.format(base_url, '/dologin.php', parameters)
    return payment_url
