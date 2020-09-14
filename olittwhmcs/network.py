"""This module contains the functions that make networks requests to whmcs."""

import requests
from requests.exceptions import RequestException

from olittwhmcs.exceptions import WhmcsConnectionError


def get_whmcs_response(parameters):
    """
    Make requests to whmcs and retrieve the response or error.
    :param parameters: (Dictionary) the request payload
    :return: whmcs response if request completed successfully otherwise an error message
    :rtype: Dictionary or String or None
    """
    try:
        response = make_whmcs_network_request(parameters)
        response_data = get_response_data(response)
        result = response_data.get('result')
        if response.ok and result == "success":
            return True, response_data
        error = get_error_message(response_data)
    except WhmcsConnectionError as e:
        error = e.message
    return False, error


def make_whmcs_network_request(parameters):
    """
    Make a network request to WHMCS.
    :param parameters: Dictionary, payload to send to whmcs
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    :raises WhmcsConnectionError: If the network request fails.
    """
    # ToDo: Read this url from consumers or settings.py (or from env variables if not possible)
    url = "https://www.olitt.com/billing/includes/api.php"
    try:
        return requests.post(url=url, data=parameters)
    except RequestException:
        raise WhmcsConnectionError("Could not reach whmcs server.")


def get_response_data(response):
    """
    Get data from a network response.
    :param response: requests.Response, the network response.
    :return: Data from the response if able to deserialize the response.
    :rtype: Dictionary or None
    """
    try:
        return response.json()
    except ValueError:
        return None


def get_error_message(response_data):
    """
    Extract an error message from whmcs response data.
    :param response_data: Dictionary, data received from whmcs from which to extract the message.
    :return: Error message in the whmcs response data.
    :rtype: String or None
    """
    if type(response_data) is dict:
        result = response_data.get('result', None)
        error = response_data.get('message', None)
        print(result)
        print(error)
        if result == "error":
            return error
    return None
