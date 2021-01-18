import pytest
import requests
import responses

from olittwhmcs import network
from olittwhmcs.exceptions import WhmcsConnectionError


################################
# make_whmcs_network_request() #
################################

@responses.activate
def test_make_whmcs_network_request_returns_the_expected_response():
    expected_response = {'error': 'not found'}
    responses.add(responses.POST, 'https://www.olitt.com/billing/includes/api.php', json=expected_response, status=404)
    response = network.make_whmcs_network_request({})
    assert type(response) is requests.Response
    assert response == responses.calls[0].response
    assert response.status_code == 404


@responses.activate
def test_make_whmcs_network_request_raises_a_whmcs_connection_error_when_an_invalid_url_is_passed():
    expected_response = {'error': 'not found'}
    responses.add(responses.POST, 'https://www.example.com/api', json=expected_response, status=404)
    with pytest.raises(WhmcsConnectionError):
        network.make_whmcs_network_request({})


#######################
# get_response_data() #
#######################

def generate_response(url, expected_response, status):
    responses.add(responses.POST, url, json=expected_response, status=status)
    response = requests.post(url)
    return response


@responses.activate
def test_get_response_data_with_a_valid_json_body_returns_the_expected_dict():
    expected_response = {'error': 'not found'}
    response = generate_response('https://www.olitt.com/billing/includes/api.php', expected_response, 404)
    response_data = network.get_response_data(response)
    assert type(response_data) is dict
    assert response_data == expected_response


@responses.activate
def test_get_response_data_with_a_blank_json_body_returns_none():
    response = generate_response('https://www.olitt.com/billing/includes/api.php', None, 204)
    response_data = network.get_response_data(response)
    assert response_data is None


#######################
# get_error_message() #
#######################

def test_get_error_message_returns_an_error_message_if_the_response_contains_an_error():
    response = {'result': "error", 'message': "Something bad happened"}
    error = network.get_error_message(response)
    assert error == "Something bad happened"


def test_get_error_message_returns_none_if_the_response_does_not_contains_an_error():
    response = {'result': "success", 'message': "Something bad happened"}
    error = network.get_error_message(response)
    assert error is None
    assert error != "Something bad happened"


def test_get_error_message_returns_none_if_the_response_is_null_or_empty():
    error = network.get_error_message(None)
    assert error is None
    error = network.get_error_message({})
    assert error is None


def test_get_error_message_returns_none_if_the_response_is_not_valid():
    response = "<html>Something bad happened</html>"
    error = network.get_error_message(response)
    assert error is None
