import os
from unittest import mock

from olittwhmcs import request_parameters


def test_whmcs_secrets_are_retrieved_correctly():
    environ_mock = mock.patch.dict(os.environ, {
        'WHMCS_IDENTIFIER_KEY': "my_identifier_key",
        'WHMCS_SECRET_KEY': "my_secret_key",
        'WHMCS_ACCESS_KEY': "my_access_key"
    })
    environ_mock.start()

    whmcs_secrets = request_parameters.get_default_parameters()
    assert whmcs_secrets['identifier'] == "my_identifier_key"
    assert whmcs_secrets['secret'] == "my_secret_key"
    assert whmcs_secrets['accesskey'] == "my_access_key"
    assert whmcs_secrets['responsetype'] == "json"

    environ_mock.stop()


def test_products_parameters_are_set_correctly():
    default_parameters = request_parameters.get_default_parameters()
    # No filters
    parameters = {**default_parameters, **{'action': 'GetProducts'}}
    assert request_parameters.get_product_request_parameters() == parameters

    # Filter with product group
    parameters = {**default_parameters, **{'action': 'GetProducts', 'gid': 2}}
    assert request_parameters.get_product_request_parameters(group_id=2) == parameters
    assert request_parameters.get_product_request_parameters(group_id=5) != parameters

    # Filter with module
    parameters = {**default_parameters, **{'action': 'GetProducts', 'module': "awesome_products"}}
    assert request_parameters.get_product_request_parameters(module="awesome_products") == parameters
    assert request_parameters.get_product_request_parameters(module="bad_products") != parameters

    # Filter with one product
    parameters = {**default_parameters, **{'action': 'GetProducts', 'pid': "1"}}
    assert request_parameters.get_product_request_parameters(product_ids=[1]) == parameters
    assert request_parameters.get_product_request_parameters(product_ids=[1, ]) == parameters
    assert request_parameters.get_product_request_parameters(product_ids=[1, 2]) != parameters

    # Filter with many products
    parameters = {**default_parameters, **{'action': 'GetProducts', 'pid': "1,2,3"}}
    assert request_parameters.get_product_request_parameters(product_ids=[1, 2, 3]) == parameters
    assert request_parameters.get_product_request_parameters(product_ids=[7, 8, 9]) != parameters

    # Combined filters
    parameters = {
        **default_parameters,
        **{'action': 'GetProducts', 'gid': 2, 'module': "awesome_products", 'pid': "1,2,3"}
    }
    assert request_parameters.get_product_request_parameters(group_id=2, module="awesome_products",
                                                             product_ids=[1, 2, 3]) == parameters
    assert request_parameters.get_product_request_parameters(group_id=20, module="awesome_products",
                                                             product_ids=[1, 2, 3]) != parameters
    assert request_parameters.get_product_request_parameters(group_id=2, module="bad_products",
                                                             product_ids=[1, 2, 3]) != parameters
    assert request_parameters.get_product_request_parameters(group_id=2, module="awesome_products",
                                                             product_ids=[1]) != parameters
