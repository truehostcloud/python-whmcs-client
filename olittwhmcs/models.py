"""Whmcs models."""


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
        self.payment_type = whmcs_product.get('paytype')
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
