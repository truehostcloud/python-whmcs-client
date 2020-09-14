"""Whmcs models."""
from datetime import datetime


class Product:
    """This object contains a whmcs product."""

    def __init__(self, whmcs_product, currency):
        """
        Deserializes the whmcs product.
        :param whmcs_product: Dictionary, the whmcs product.
        :param currency: String, name of currency to show prices in. Eg ksh, usd
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
        """
        Deserializes the whmcs client product.
        :param whmcs_product: Dictionary, the whmcs product.
        """
        self.id = whmcs_product.get('id')
        self.client_id = whmcs_product.get('clientid')
        self.order_id = whmcs_product.get('orderid')
        self.product_id = whmcs_product.get('pid')
        self.registration_date = get_date_object(whmcs_product.get('regdate'), '%Y-%m-%d')
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
        self.next_due_date = get_date_object(whmcs_product.get('nextduedate'), '%Y-%m-%d')
        self.status = whmcs_product.get('status')
        self.notes = whmcs_product.get('notes')


def get_date_object(date: str, date_format: str):
    """ Convert a string into a date object. """
    try:
        return datetime.strptime(date, date_format)
    except ValueError:
        return None
