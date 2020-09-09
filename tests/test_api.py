import pytest
import requests
import responses
from olittwhmcs import api
from olittwhmcs.exceptions import WhmcsConnectionError

"""
Test api.make_whmcs_network_request()
- test valid response is returned is everything is ok
- test a WhmcsConnectionError is raised if an invalid url is passed
"""


@responses.activate
def test_whmcs_response_is_returned_correctly():
    responses.add(responses.POST, 'https://www.example.com/api', json={'error': 'not found'}, status=404)
    responses.add(responses.POST, 'https://www.example.com/api/create', json={'id': 1}, status=200)

    whmcs_response = api.make_whmcs_network_request('https://www.example.com/api', {})
    assert whmcs_response == responses.calls[0].response
    assert whmcs_response.status_code == 404

    whmcs_response = api.make_whmcs_network_request('https://www.example.com/api/create', {})
    assert whmcs_response == responses.calls[1].response
    assert whmcs_response.status_code == 200


@responses.activate
def test_whmcs_response_is_return_a_whmcs_connection_error_when_an_invalid_url_is_passed():
    expected_response = {'error': 'not found'}
    responses.add(responses.POST, 'https://www.example.com/api', json=expected_response, status=404)

    with pytest.raises(WhmcsConnectionError):
        api.make_whmcs_network_request('https://www.idontexist.com/api', {})


"""
Test api.get_response_data()
- test with valid json body
- test with invalid valid json body
- test with empty body
"""


@responses.activate
def test_get_response_data_with_a_valid_json_body():
    url = 'https://www.olitt.com/billing/includes/api.php'
    expected_response = {'error': 'not found'}
    responses.add(responses.POST, url, json=expected_response, status=404)
    response = requests.post(url)
    assert type(api.get_response_data(response)) == dict
    assert api.get_response_data(response) == expected_response
    assert api.get_response_data(response) is not None
    assert api.get_response_data(response) != {}
    assert api.get_response_data(response) != ""


@responses.activate
def test_get_response_data_with_a_invalid_json_body():
    url = 'https://www.olitt.com/billing/includes/api.php'
    expected_response = "some html response"
    responses.add(responses.POST, url, json=expected_response, status=404)
    response = requests.post(url)
    assert api.get_response_data(response) == expected_response
    # assert api.get_response_data(response) is None
    assert api.get_response_data(response) != {}
    assert api.get_response_data(response) != ""


@responses.activate
def test_get_response_data_with_a_blank_json_body():
    url = 'https://www.olitt.com/billing/includes/api.php'
    responses.add(responses.POST, url, json=None, status=204)
    response = requests.post(url)
    assert api.get_response_data(response) is None
    assert api.get_response_data(response) != {'key': "value"}
    assert api.get_response_data(response) != {}
    assert api.get_response_data(response) != ""
