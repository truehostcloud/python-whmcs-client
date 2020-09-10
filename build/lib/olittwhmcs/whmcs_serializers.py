import re

from affiliate.models import Affiliate
from billing.models import BillingAccount, Order, PaymentMethod, OrderItem, Transaction, Invoice
from sitebuilder.exceptions import OlittSerializationException
from sitebuilder.utilities import get_date_object


def deserialize_whmcs_billing_account_id(whmcs_client_id: dict) -> int:
    try:
        return whmcs_client_id.get('clientid')
    except Exception as e:
        raise OlittSerializationException(whmcs_client_id, int, description=e.__str__())


def deserialize_whmcs_billing_account(whmcs_client: dict) -> BillingAccount:
    try:
        whmcs_client = whmcs_client.get('client')
        return BillingAccount(
            id=whmcs_client.get('userid'),
            user=None,
            status=whmcs_client.get('status'),

            first_name=whmcs_client.get('firstname'),
            last_name=whmcs_client.get('lastname'),
            email=whmcs_client.get('email'),
            phone={'country': int(whmcs_client.get('phonecc')), 'msisdn': int(whmcs_client.get('phonenumber'))},

            address=whmcs_client.get('address1'),
            city=whmcs_client.get('city'),
            state=whmcs_client.get('fullstate'),
            postcode=whmcs_client.get('postcode'),
            country=whmcs_client.get('countryname'),

            currency=whmcs_client.get('currency_code')
        )
    except Exception as e:
        raise OlittSerializationException(whmcs_client, BillingAccount(), description=e.__str__())


def deserialize_whmcs_order_id(whmcs_order_id: dict) -> int:
    try:
        return whmcs_order_id.get('orderid')
    except Exception as e:
        raise OlittSerializationException(whmcs_order_id, int, description=e.__str__())


def deserialize_whmcs_orders(whmcs_orders: dict, billing_account: BillingAccount) -> list:
    try:
        orders = []
        whmcs_order_container = whmcs_orders.get('orders', [])
        if type(whmcs_order_container) is list:
            whmcs_order_container = {}
        whmcs_order_list = whmcs_order_container.get('order', [])
        for whmcs_order in whmcs_order_list:
            orders.append(deserialize_whmcs_order(whmcs_order, billing_account))
        return list(filter(None, orders))
    except Exception as e:
        raise OlittSerializationException(whmcs_orders, list, description=e.__str__())


def deserialize_whmcs_order(whmcs_order: dict, billing_account: BillingAccount) -> Order:
    try:
        return Order(
            ordered_by=billing_account,
            id=whmcs_order.get('id'),
            order_number=whmcs_order.get('ordernum'),
            date=get_date_object(whmcs_order.get('date'), '%Y-%m-%d %H:%M:%S'),
            amount=float(whmcs_order.get('amount')),
            invoice_id=whmcs_order.get('invoiceid'),
            order_status=whmcs_order.get('status'),
            payment_status=whmcs_order.get('paymentstatus'),
            payment_method=PaymentMethod(
                method=whmcs_order.get('paymentmethod'),
                display_name=whmcs_order.get('paymentmethodname'),
                logo=None
            ),
            order_items=deserialize_whmcs_order_items(whmcs_order)
        )
    except Exception as e:
        raise OlittSerializationException(whmcs_order, Order(), description=e.__str__())


def deserialize_whmcs_order_items(whmcs_order_items: dict) -> list:
    try:
        order_items = []
        whmcs_order_items_container = whmcs_order_items.get('lineitems', [])
        if type(whmcs_order_items_container) is list:
            whmcs_order_items_container = {}
        whmcs_order_item_list = whmcs_order_items_container.get('lineitem', [])
        for whmcs_order_item in whmcs_order_item_list:
            order_items.append(deserialize_whmcs_order_item(whmcs_order_item))
        return list(filter(None, order_items))

    except Exception as e:
        raise OlittSerializationException(whmcs_order_items, list, description=e.__str__())


def deserialize_whmcs_order_item(whmcs_order_item: dict) -> OrderItem:
    try:
        return OrderItem(
            item_type=whmcs_order_item.get('type'),
            product_type=whmcs_order_item.get('producttype'),
            product=whmcs_order_item.get('product'), domain=whmcs_order_item.get('domain'),
            billing_cycle=whmcs_order_item.get('billingcycle'),
            amount=float(re.compile(r'\d+(?:\.\d+)?').findall(whmcs_order_item.get('amount'))[0]),
            status=whmcs_order_item.get('status')
        )
    except Exception as e:
        raise OlittSerializationException(whmcs_order_item, OrderItem(), description=e.__str__())


def deserialize_whmcs_payment_methods(whmcs_payment_methods: dict) -> list:
    try:
        payment_methods = []
        whmcs_payment_methods_container = whmcs_payment_methods.get('paymentmethods', [])
        if type(whmcs_payment_methods_container) is list:
            whmcs_payment_methods_container = {}
        whmcs_payment_method_list = whmcs_payment_methods_container.get('paymentmethod', [])
        for whmcs_payment_method in whmcs_payment_method_list:
            payment_methods.append(deserialize_whmcs_payment_method(whmcs_payment_method))
        return list(filter(None, payment_methods))
    except Exception as e:
        raise OlittSerializationException(whmcs_payment_methods, list, description=e.__str__())


def deserialize_whmcs_payment_method(whmcs_payment_method: dict) -> PaymentMethod:
    try:
        return PaymentMethod(
            method=whmcs_payment_method.get('module'),
            display_name=whmcs_payment_method.get('displayname'),
            logo=None
        )
    except Exception as e:
        raise OlittSerializationException(whmcs_payment_method, PaymentMethod(), description=e.__str__())


def deserialize_whmcs_transactions(whmcs_transactions: dict) -> list:
    try:
        transactions = []
        whmcs_transactions_container = whmcs_transactions.get('transactions', [])
        if type(whmcs_transactions_container) is list:
            whmcs_transactions_container = {}
        whmcs_transaction_list = whmcs_transactions_container.get('transaction', [])
        for whmcs_transaction in whmcs_transaction_list:
            transactions.append(deserialize_whmcs_transaction(whmcs_transaction))
        return list(filter(None, transactions))
    except Exception as e:
        raise OlittSerializationException(whmcs_transactions, list, description=e.__str__())


def deserialize_whmcs_transaction(whmcs_transaction: dict) -> Transaction:
    try:
        amount_in = whmcs_transaction.get('amountin', "0.00")
        amount_out = whmcs_transaction.get('amountout', "0.00")
        amount = amount_in if amount_in != "0.00" else amount_out
        transaction_type = "Deposit" if amount_in != "0.00" else "Withdrawal"
        return Transaction(
            id=whmcs_transaction.get('id', None),
            invoice=Invoice(pk=whmcs_transaction.get('invoiceid')),
            refund_id=whmcs_transaction.get('refundid'),
            transaction_id=whmcs_transaction.get('transid'),
            payment_method=whmcs_transaction.get('gateway'),
            description=whmcs_transaction.get('description'),
            date=get_date_object(whmcs_transaction.get('date'), '%Y-%m-%d %H:%M:%S'),
            amount=amount,
            transaction_type=transaction_type,
            fees=whmcs_transaction.get('fees'),
            rate=whmcs_transaction.get('rate')
        )
    except Exception as e:
        raise OlittSerializationException(whmcs_transaction, Transaction(), description=e.__str__())


def deserialize_whmcs_invoices(whmcs_invoices: dict, get_orders, get_transactions) -> list:
    try:
        invoices = []
        whmcs_invoices_container = whmcs_invoices.get('invoices', [])
        if type(whmcs_invoices_container) is list:
            whmcs_invoices_container = {}
        whmcs_invoice_list = whmcs_invoices_container.get('invoice', [])
        if whmcs_invoice_list:
            # ToDo: Execute parameter functions to fetch all user orders and transactions
            my_orders = get_orders
            my_transactions = get_transactions
            for whmcs_invoice in whmcs_invoice_list:
                invoice_id = whmcs_invoice.get('id')
                invoice_orders = [order for order in my_orders if order.invoice_id == invoice_id]
                invoice_transactions = [trx for trx in my_transactions if trx.invoice_id == invoice_id]
                if invoice_orders:
                    invoice_order = invoice_orders[0]
                    invoices.append(deserialize_whmcs_invoice(whmcs_invoice, invoice_order, invoice_transactions))
        return list(filter(None, invoices))
    except Exception as e:
        raise OlittSerializationException(whmcs_invoices, list, description=e.__str__())


def deserialize_whmcs_invoice(whmcs_invoice: dict, order: Order, transactions: list) -> Invoice:
    try:
        return Invoice(
            id=whmcs_invoice.get('id'),
            first_name=whmcs_invoice.get('firstname'),
            last_name=whmcs_invoice.get('lastname'),
            date_created=get_date_object(whmcs_invoice.get('date'), '%Y-%m-%d'),
            date_due=get_date_object(whmcs_invoice.get('duedate'), '%Y-%m-%d'),
            date_paid=get_date_object(whmcs_invoice.get('datepaid'), '%Y-%m-%d %H:%M:%S'),
            sub_total=float(whmcs_invoice.get('subtotal')),
            credit=float(whmcs_invoice.get('credit')),
            total=float(whmcs_invoice.get('total')),
            status=whmcs_invoice.get('status'),
            order=order,
            transactions=transactions
        )
    except Exception as e:
        raise OlittSerializationException(whmcs_invoice, Invoice(), description=e.__str__())


def deserialize_whmcs_domain_availability_status(whmcs_domain_availability_info: dict) -> bool:
    try:
        status = whmcs_domain_availability_info.get('status')
        return status == 'available'
    except Exception as e:
        raise OlittSerializationException(whmcs_domain_availability_info, bool, description=e.__str__())


def deserialize_whmcs_domain_prices_for_tld(tld: str, whmcs_domain_prices: dict) -> dict:
    try:
        if tld is not None:
            pricing = whmcs_domain_prices.get('pricing')
            tld_prices = pricing.get(tld)
            return {
                'register': float(tld_prices.get('register', {}).get('1')),
                'renew': float(tld_prices.get('renew', {}).get('1')),
                'transfer': float(tld_prices.get('transfer', {}).get('1'))
            }
        status = whmcs_domain_prices.get('status')
        return status == "available"
    except Exception as e:
        raise OlittSerializationException(whmcs_domain_prices, dict, description=e.__str__())


def deserialize_whmcs_domains(whmcs_domains: dict) -> list:
    try:
        domains = []
        whmcs_domains_container = whmcs_domains.get('domains', "")
        if type(whmcs_domains_container) is str:
            whmcs_domains_container = {}
        whmcs_domain_list = whmcs_domains_container.get('domain', [])
        for whmcs_domain in whmcs_domain_list:
            domains.append(deserialize_whmcs_domain(whmcs_domain))
        return list(filter(None, domains))
    except Exception as e:
        raise OlittSerializationException(whmcs_domains, list, description=e.__str__())


def deserialize_whmcs_domain(whmcs_domain: dict) -> dict:
    try:
        return {
            'id': whmcs_domain.get('id', None),
            'domain_name': whmcs_domain.get('domainname', None),
            'registration_period': whmcs_domain.get('regperiod', None),
            'purchase_price': whmcs_domain.get('firstpaymentamount', None),
            'renewal_price': whmcs_domain.get('recurringamount', None),
            'payment_method': whmcs_domain.get('paymentmethodname', None),
            'date_due': {
                'year': whmcs_domain.get('nextduedate', "").split('-')[0],
                'month': whmcs_domain.get('nextduedate', "").split('-')[1],
                'day': whmcs_domain.get('nextduedate', "").split('-')[2]
            },
            'status': whmcs_domain.get('status', None)
        }
    except Exception as e:
        raise OlittSerializationException(whmcs_domain, dict, description=e.__str__())


def deserialize_whmcs_affiliates(whmcs_affiliates: dict) -> list:
    try:
        affiliates = []
        whmcs_affiliates_container = whmcs_affiliates.get('affiliates', [])
        if type(whmcs_affiliates_container) is list:
            whmcs_affiliates_container = {}
        whmcs_affiliate_list = whmcs_affiliates_container.get('affiliate', [])
        for whmcs_affiliate in whmcs_affiliate_list:
            affiliates.append(deserialize_whmcs_affiliate(whmcs_affiliate))
        return list(filter(None, affiliates))
    except OlittSerializationException as e:
        raise e
    except Exception as e:
        raise OlittSerializationException(whmcs_affiliates, list, description=e.__str__())


def deserialize_whmcs_affiliate(whmcs_affiliate: dict) -> Affiliate:
    try:
        affiliates = Affiliate(
            id=whmcs_affiliate.get('id'),
            affiliate_id=whmcs_affiliate.get('id'),
            date_enrolled=get_date_object(whmcs_affiliate.get('date'), '%Y-%m-%d'),
            visitors=whmcs_affiliate.get('visitors'),
            balance=float(whmcs_affiliate.get('balance')),
            withdrawn=float(whmcs_affiliate.get('withdrawn'))
        )
        return affiliates
    except Exception as e:
        raise OlittSerializationException(whmcs_affiliate, Affiliate(), description=e.__str__())
