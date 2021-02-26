"""This module contains the api surface for consuming this package."""

from datetime import datetime
import hashlib
import os
import time

from olittwhmcs import serializer, models
from olittwhmcs.exceptions import WhmcsException
from olittwhmcs.models import Product, ClientProduct, Client
from olittwhmcs.network import get_whmcs_response
from olittwhmcs.serializer import get_product_request_parameters, \
    order_product_request_parameters, \
    create_user_request_parameters, get_client_product_request_parameters, \
    upgrade_product_request_parameters, prepare_get_invoices_request, \
    prepare_get_orders_request, prepare_cancel_order_request, \
    order_domain_request_parameters, order_bulk_products_request_parameters, get_domain_nameservers_request_parameter, \
    update_domain_nameservers_request_parameter


##########
# CLIENT #
##########

def create_client(**kwargs):
    """Create a WHMCS User account.

    Args:
        kwargs: Keyword arguments with user details.
            first_name, last_name, email, country, state, city, postcode, address,
            phone, password
    Returns:
        list: products retrieved from whmcs
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = create_user_request_parameters(**kwargs)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        client_id = response_or_error.get('clientid')
        return client_id
    default_error = "Unable to enroll for a billing account"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def get_client(email=None, client_id=None):
    """Retrieve a WHMCS User account.

    Args:
        email (str): (Optional) email of client to retrieve.
        client_id (int): (Optional) id of client to retrieve.
    Returns:
        Client: The client retrieved from whmcs
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = serializer.get_client_request_parameters(email, client_id)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        client = Client(response_or_error)
        return client
    default_error = "Unable to get client details"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def update_client(**kwargs):
    """Update a WHMCS User account.
       Args:
        kwargs: Keyword arguments with user details.
            first_name, last_name, email, country, state, city, postcode, address,
            phone, password
        Returns:
            list: products retrieved from whmcs
        Raises:
            WhmcsException: If an error occurs.
    """
    parameters = serializer.update_client_request_parameters(**kwargs)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        client_id = response_or_error.get('clientid')
        return client_id
    default_error = "Unable to update client details"
    raise WhmcsException(response_or_error if response_or_error else default_error)


###########
# PRODUCT #
###########

def get_products(currency=None, group_id=None, module=None, product_ids=None):
    """Retrieve products from WHMCS.

    Args:
        currency (str): Optional. Currency to display prices. Eg kes, usd.
        group_id (int): Optional. ID of the group from which to fetch products.
        module (str): Optional. Name of the module from which to fetch products.
        product_ids (list): Optional. Product ids to retrieve.
    Returns:
        list: Products retrieved from whmcs
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = get_product_request_parameters(group_id, module, product_ids)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        try:
            whmcs_products_wrapper = response_or_error.get('products', '')
            whmcs_products = whmcs_products_wrapper.get('product')
        except AttributeError:
            whmcs_products = []

        products = []
        for whmcs_product in whmcs_products:
            product = Product(whmcs_product, currency)
            products.append(product)
        return products
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def get_client_products(client_id, product_id=None, service_id=None, domain=None):
    """
    Retrieve a user's products from WHMCS.
    :param client_id: Integer, id of the client whose products to fetch.
    :param product_id: Integer, specific product id to obtain the details for.
    :param service_id: Integer, specific service id to obtain the details for.
    :param domain: String, specific domain to obtain the service details for.
    """
    parameters = get_client_product_request_parameters(client_id, product_id,
                                                       service_id, domain)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful:
        try:
            whmcs_products_wrapper = response_or_error.get('products', '')
            whmcs_products = whmcs_products_wrapper.get('product', [])
        except AttributeError:
            whmcs_products = []

        client_products = []
        for whmcs_product in whmcs_products:
            client_product = ClientProduct(whmcs_product)
            client_products.append(client_product)
        return client_products
    default_error = "Unable to fetch your products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def order_product(client_id, payment_method, billing_cycle, product_id=None,
                  domain=None, **kwargs):
    """
    Place a product order in WHMCS.
    :param client_id: Integer, id of the client placing the order.
    :param product_id: Integer, id of the product to order.
    :param domain: Integer, domain name to order.
    :param payment_method: String, preferred method of paying for the order.
        Eg, paypal, rave, ...
    :param billing_cycle: String, billing cycle. Eg, monthly, annually
    :param kwargs: (Optional) Other parameters to add to the order payload.
        Eg promo_code, affiliate_id, price (override), ...
    :return: id of placed order, id of corresponding invoice
    :rtype: int, int
    :raises WhmcsException: If an error occurs.
    """
    if product_id:
        parameters = order_product_request_parameters(client_id, product_id,
                                                      payment_method, billing_cycle,
                                                      **kwargs)
    else:
        parameters = order_domain_request_parameters(client_id, domain, payment_method,
                                                     billing_cycle, **kwargs)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        order_id = response_or_error.get('orderid')
        invoice_id = response_or_error.get('invoiceid')
        return order_id, invoice_id
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def order_bulk_products(parameters=None, **kwargs):
    """
    Place a multiple products order in WHMCS.
    :param parameters: dict of the order placed.
    :param product_id: Integer, id of the product to order.
    :param kwargs: (Optional) Other parameters to add to the order payload.
        Eg promo_code, affiliate_id, price (override), ...
    :return: id of placed order, id of corresponding invoice
    :rtype: int, int
    :raises WhmcsException: If an error occurs.
    """
    if not parameters:
        parameters = {}
    updated_parameters = order_bulk_products_request_parameters(parameters)
    is_successful, response_or_error = get_whmcs_response(updated_parameters)
    if is_successful and response_or_error:
        order_id = response_or_error.get('orderid')
        invoice_id = response_or_error.get('invoiceid')
        return order_id, invoice_id
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def get_domain_nameservers(domain_id):
    """get  domain nameservers.

       Args:
           domain_id (int): The Id of the domain.
       Returns:
           dict: the nameservers of the domain
       Raises:
           WhmcsException: If an error occurs.
   """
    parameters = get_domain_nameservers_request_parameter(domain_id)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        return response_or_error
    default_error = "Unable to get nameservers"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def update_domain_nameservers(data):
    """update a domain nameservers.

        Args:
            data (dict): data containing the nameservers and domain id.
        Returns:
            dict: the results of the update of nameserver
        Raises:
            WhmcsException: If an error occurs.
    """
    parameters = update_domain_nameservers_request_parameter(data)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        return response_or_error
    default_error = "Unable to update nameservers"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def upgrade_client_product(service_id, payment_method, billing_cycle=None,
                           package_id=None):
    """Upgrade a product in WHMCS.

    Args:
        service_id (int): ID of the service to update.
        payment_method (str): Preferred method of paying for the upgrade.
            Eg, paypal, rave, ...
        billing_cycle (str): (Optional), new product's billing cycle.
        package_id (int): (Optional), package ID to associate with the service.
    Returns:
        Client: The client retrieved from whmcs
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = upgrade_product_request_parameters(service_id, payment_method,
                                                    billing_cycle, package_id)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        service_id = response_or_error.get('serviceid')
        return service_id
    default_error = "Unable to fetch products"
    raise WhmcsException(response_or_error if response_or_error else default_error)


###########
# SERVICE #
###########

def upgrade_product(service_id, payment_method, upgrade_type, new_product_id=None,
                    new_billing_cycle=None, promo_code=None):
    """Upgrade, or calculate an upgrade on, a product.

    Args:
        service_id (int): ID of the service to update.
        payment_method (str): Upgrade payment method in system format (e.g. paypal).
        upgrade_type (str): Type of upgrade (product, configoptions).
        new_product_id (int): Optional. ID of the new product.
        new_billing_cycle (str): Optional. New products billing cycle.
        promo_code (str): Optional. Promotion code to apply to the upgrade.
    Returns:
        ProductUpgrade: Instance of 'upgrade product' response.
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = serializer.get_upgrade_product_parameters(service_id, payment_method,
                                                           upgrade_type, new_product_id,
                                                           new_billing_cycle,
                                                           promo_code)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        return models.ProductUpgrade(response_or_error)
    default_error = "Unable to complete upgrade"
    raise WhmcsException(response_or_error if response_or_error else default_error)


#########
# ORDER #
#########

def get_orders(client_id=None, order_id=None, status=None):
    """Retrieve a WHMCS orders.

    Args:
        client_id (int): (Optional) ID of client whose orders to retrieve.
        order_id (int): (Optional) ID of the order retrieve.
        status (str): (Optional) Status of the order to retrieve.
    Returns:
        list: Orders retrieved from whmcs
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = prepare_get_orders_request(client_id, order_id, status)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        try:
            whmcs_orders_wrapper = response_or_error.get('orders')
            whmcs_orders = whmcs_orders_wrapper.get('order')
        except AttributeError:
            whmcs_orders = []

        orders = []
        for whmcs_order in whmcs_orders:
            order = models.Order(whmcs_order)
            orders.append(order)
        return orders
    default_error = "Unable to fetch orders"
    raise WhmcsException(response_or_error if response_or_error else default_error)


def cancel_order(order_id, cancel_subscription=None, no_email=None):
    """Cancel a WHMCS order.

    Args:
        order_id (int): (Optional) ID of the order to cancel.
        cancel_subscription (bool): (Optional) Attempts to cancel the subscription
            associated with the product if True.
        no_email (bool): (Optional) Stops the invoice payment email from being sent if
            the invoice becomes paid if True.
    Returns:
        bool: True if order was cancelled, False otherwise.
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = prepare_cancel_order_request(order_id, cancel_subscription, no_email)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful:
        return is_successful
    default_error = "Unable to cancel the order"
    raise WhmcsException(response_or_error if response_or_error else default_error)


###########
# INVOICE #
###########

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

    base_url = os.environ.get('WHMCS_CLIENT_AREA_URL', 'https://www.olitt.com/billing')

    invoice_url = '{}{}?id={}'.format(base_url, '/viewinvoice.php', invoice_id)
    parameters = 'email={}&timestamp={}&hash={}&goto={}'.format(client_email,
                                                                get_timestamp(),
                                                                whmcs_hash, invoice_url)
    payment_url = '{}{}?{}'.format(base_url, '/dologin.php', parameters)
    return payment_url


def get_invoices(client_id=None, status=None, order_by=None, order=None):
    """Retrieve a WHMCS invoices.

    Args:
        client_id (int): (Optional) ID of client whose invoices to retrieve.
        status (str): (Optional) Status of the invoices to retrieve.
        order (str): (Optional) Sort attribute. Accepted values are: asc, desc.
        order_by (str): (Optional) Field to sort results by. Accepted values are:
            id, invoicenumber, date, duedate, total, status.
    Returns:
        list: Invoices retrieved from whmcs
    Raises:
        WhmcsException: If an error occurs.
    """
    parameters = prepare_get_invoices_request(client_id, status, order_by, order)
    is_successful, response_or_error = get_whmcs_response(parameters)
    if is_successful and response_or_error:
        try:
            whmcs_invoices_wrapper = response_or_error.get('invoices')
            whmcs_invoices = whmcs_invoices_wrapper.get('invoice')
        except AttributeError:
            whmcs_invoices = []

        invoices = []
        for whmcs_invoice in whmcs_invoices:
            invoice = models.Invoice(whmcs_invoice)
            invoices.append(invoice)
        return invoices
    default_error = "Unable to fetch invoices"
    raise WhmcsException(response_or_error if response_or_error else default_error)
