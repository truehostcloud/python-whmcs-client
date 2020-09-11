import os
from unittest import mock

from olittwhmcs import serializer


############################
# get_default_parameters() #
############################

def test_whmcs_secrets_are_retrieved_correctly():
    environ_mock = mock.patch.dict(os.environ, {
        'WHMCS_IDENTIFIER_KEY': "my_identifier_key",
        'WHMCS_SECRET_KEY': "my_secret_key",
        'WHMCS_ACCESS_KEY': "my_access_key"
    })
    environ_mock.start()
    whmcs_secrets = serializer.get_default_parameters()
    environ_mock.stop()

    assert whmcs_secrets['identifier'] == "my_identifier_key"
    assert whmcs_secrets['secret'] == "my_secret_key"
    assert whmcs_secrets['accesskey'] == "my_access_key"
    assert whmcs_secrets['responsetype'] == "json"


####################################
# get_product_request_parameters() #
####################################

def test_products_parameters_are_retrieved_correctly_without_any_filters():
    default_parameters = serializer.get_default_parameters()
    parameters = {**default_parameters, **{'action': 'GetProducts'}}
    assert serializer.get_product_request_parameters() == parameters


def test_products_parameters_are_retrieved_correctly_with_a_group_filter():
    default_parameters = serializer.get_default_parameters()
    parameters = {**default_parameters, **{'action': 'GetProducts', 'gid': 2}}
    assert serializer.get_product_request_parameters(group_id=2) == parameters
    assert serializer.get_product_request_parameters(group_id=5) != parameters


def test_products_parameters_are_retrieved_correctly_with_a_module_filter():
    default_parameters = serializer.get_default_parameters()
    parameters = {**default_parameters, **{'action': 'GetProducts', 'module': "awesome_products"}}
    assert serializer.get_product_request_parameters(module="awesome_products") == parameters
    assert serializer.get_product_request_parameters(module="bad_products") != parameters


def test_products_parameters_are_retrieved_correctly_with_a_single_product_filter():
    default_parameters = serializer.get_default_parameters()
    parameters = {**default_parameters, **{'action': 'GetProducts', 'pid': "1"}}
    assert serializer.get_product_request_parameters(product_ids=[1]) == parameters
    assert serializer.get_product_request_parameters(product_ids=[1, ]) == parameters
    assert serializer.get_product_request_parameters(product_ids=[1, 2]) != parameters


def test_products_parameters_are_retrieved_correctly_with_a_multiple_product_filters():
    default_parameters = serializer.get_default_parameters()
    parameters = {**default_parameters, **{'action': 'GetProducts', 'pid': "1,2,3"}}
    assert serializer.get_product_request_parameters(product_ids=[1, 2, 3]) == parameters
    assert serializer.get_product_request_parameters(product_ids=[7, 8, 9]) != parameters


def test_products_parameters_are_retrieved_correctly_with_combined_filters():
    default_parameters = serializer.get_default_parameters()
    default_parameters.update({'action': 'GetProducts', 'gid': 2, 'module': "awesome_products", 'pid': "1,2,3"})
    params = serializer.get_product_request_parameters(group_id=2, module="awesome_products", product_ids=[1, 2, 3])
    assert params == default_parameters
    params = serializer.get_product_request_parameters(group_id=2, module="other_products", product_ids=[1, 2, 3])
    assert params != default_parameters
