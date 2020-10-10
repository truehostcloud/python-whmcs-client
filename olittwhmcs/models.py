"""Whmcs models."""

from datetime import datetime


class Client:
    """This object contains a whmcs client."""

    def __init__(self, whmcs_client):
        """Deserializes the whmcs client.

        Args:
            whmcs_client (dict): Response obtained from whmcs.
        """
        client = whmcs_client.get('client')
        self.id = client.get('id')
        self.uuid = client.get('uuid')
        self.first_name = client.get('firstname')
        self.last_name = client.get('lastname')
        self.email = client.get('email')
        self.phone_country_code = client.get('phonecc')
        self.phone_number = client.get('telephoneNumber')
        self.company = client.get('companyname')
        self.address = client.get('address1')
        self.postcode = client.get('postcode')
        self.city = client.get('city')
        self.state = client.get('state')
        self.country = client.get('country')
        self.currency_id = client.get('currency')
        self.currency_code = client.get('currency_code')


class Product:
    """This object contains a whmcs product."""

    def __init__(self, whmcs_product, currency):
        """Deserializes the whmcs product.

        Args:
            whmcs_product (dict): Response obtained from whmcs.
            currency (str): Currency to get prices in.
        """
        self.id = whmcs_product.get('pid')
        self.group_id = whmcs_product.get('gid')
        self.module = whmcs_product.get('module')
        self.type = whmcs_product.get('type')
        self.name = whmcs_product.get('name')
        self.description = whmcs_product.get('description')
        self.billing_cycle = whmcs_product.get('paytype')
        whmcs_pricing = whmcs_product.get('pricing')
        self.pricing = self.get_pricing(whmcs_pricing, currency)

    @staticmethod
    def get_pricing(whmcs_pricing, currency):
        default_pricing_object = whmcs_pricing.get('USD', {})
        pricing_object = whmcs_pricing.get(currency.upper(), default_pricing_object)
        return {
            'prefix': pricing_object.get('prefix'),
            'monthly': float(pricing_object.get('monthly')),
            'quarterly': float(pricing_object.get('quarterly')),
            'semiannually': float(pricing_object.get('semiannually')),
            'annually': float(pricing_object.get('annually')),
            'biennially': float(pricing_object.get('biennially')),
            'triennially': float(pricing_object.get('triennially')),
        }


class ClientProduct:
    """This object contains a whmcs client's product."""

    def __init__(self, whmcs_product):
        """Deserializes the whmcs client product.

        Args:
            whmcs_product (dict): The whmcs product.
        """
        self.id = whmcs_product.get('id')
        self.client_id = whmcs_product.get('clientid')
        self.order_id = whmcs_product.get('orderid')
        self.product_id = whmcs_product.get('pid')
        self.registration_date = get_date_object(whmcs_product.get('regdate'),
                                                 '%Y-%m-%d')
        self.name = whmcs_product.get('name')
        self.translated_name = whmcs_product.get('translated_name')
        self.group_name = whmcs_product.get('groupname')
        self.translated_group_name = whmcs_product.get('translated_groupname')
        self.suspension_reason = whmcs_product.get('suspensionreason')
        self.first_payment_amount = whmcs_product.get('firstpaymentamount')
        self.recurring_amount = whmcs_product.get('recurringamount')
        self.payment_method = whmcs_product.get('payment_method')
        self.payment_method_name = whmcs_product.get('paymentmethodname')
        self.billing_cycle = whmcs_product.get('billingcycle')
        self.next_due_date = get_date_object(whmcs_product.get('nextduedate'),
                                             '%Y-%m-%d')
        self.status = whmcs_product.get('status')
        self.notes = whmcs_product.get('notes')


def get_date_object(date: str, date_format: str):
    """ Convert a string into a date object. """
    try:
        return datetime.strptime(date, date_format)
    except ValueError:
        return None


class ProductUpgrade:
    """Deserialize upgrade product response."""

    def __init__(self, response):
        """Obtain values from dictionary and store in instance."""
        self.id = response.get('id')
        self.old_product_id = response.get('oldproductid')
        self.old_product_name = response.get('oldproductname')
        self.new_product_id = response.get('newproductid')
        self.new_product_name = response.get('newproductid')
        self.new_product_billing_cycle = response.get('newproductbillingcycle')
        self.days_until_renewal = response.get('daysuntilrenewal')
        self.price = response.get('price')
        self.order_id = response.get('orderid')
        self.order_number = response.get('order_number')
        self.invoice_id = response.get('invoiceid')


class Order:
    """This object contains a whmcs invoice."""

    def __init__(self, whmcs_order):
        """Deserializes the whmcs order.

        Args:
            whmcs_order (dict): Response obtained from whmcs.
        """
        self.id = whmcs_order.get('id')
        self.order_number = whmcs_order.get('ordernum')
        self.order_data = whmcs_order.get('orderdata')
        self.client_id = whmcs_order.get('userid')

        self.date = get_date_object(whmcs_order.get('date'), '%Y-%m-%d %H:%M:%S')

        self.nameservers = (whmcs_order.get('nameservers'))
        self.transfer_secret = (whmcs_order.get('transfersecret'))
        self.renewals = whmcs_order.get('renewals')

        self.promo_code = whmcs_order.get('promocode')
        self.promo_type = whmcs_order.get('promotype')
        self.promo_value = whmcs_order.get('promovalue')

        self.amount = whmcs_order.get('amount')
        self.invoice_id = whmcs_order.get('invoiceid')
        self.payment_status = whmcs_order.get('paymentstatus')
        self.payment_method = whmcs_order.get('paymentmethod')

        self.fraud_module = whmcs_order.get('fraudmodule')
        self.fraud_output = whmcs_order.get('fraudoutput')
        self.fraud_data = whmcs_order.get('frauddata')

        self.status = whmcs_order.get('status')
        self.notes = whmcs_order.get('notes')


class Invoice:
    """This object contains a whmcs invoice."""

    def __init__(self, whmcs_invoice):
        """Deserializes the whmcs invoice.

        Args:
            whmcs_invoice (dict): Response obtained from whmcs.
        """
        self.id = whmcs_invoice.get('id')
        self.invoice_number = whmcs_invoice.get('invoicenum')
        self.client_id = whmcs_invoice.get('userid')

        self.date_created = get_date_object(whmcs_invoice.get('date'), '%Y-%m-%d')
        self.date_due = get_date_object(whmcs_invoice.get('duedate'), '%Y-%m-%d')
        self.date_paid = get_date_object(
            whmcs_invoice.get('datepaid'),
            '%Y-%m-%d %H:%M:%S')
        self.last_capture_attempt = get_date_object(
            whmcs_invoice.get('last_capture_attempt'),
            '%Y-%m-%d %H:%M:%S')

        self.sub_total = float(whmcs_invoice.get('subtotal'))
        self.total = float(whmcs_invoice.get('total'))
        self.credit = float(whmcs_invoice.get('credit'))

        self.tax = float(whmcs_invoice.get('tax'))
        self.tax2 = float(whmcs_invoice.get('tax2'))
        self.tax_rate = float(whmcs_invoice.get('taxrate'))
        self.tax_rate_2 = float(whmcs_invoice.get('taxrate2'))

        self.status = whmcs_invoice.get('status')
        self.payment_method = whmcs_invoice.get('paymentmethod')
        self.notes = whmcs_invoice.get('notes')
