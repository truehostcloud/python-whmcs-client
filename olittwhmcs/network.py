"""
This module contains the functions that make networks requests to whmcs
"""

import requests
from olittwhmcs.exceptions import WhmcsConnectionError
from requests.exceptions import ConnectionError, RequestException


def get_whmcs_response(url, parameters):
    try:
        response = make_whmcs_network_request(url, parameters)
        response_data = get_response_data(response)
        if response.ok:
            return True, response_data
        error = get_error_message(response_data)
    except WhmcsConnectionError as e:
        error = e.message
    return False, error


def make_whmcs_network_request(url, parameters):
    """
    Make a network request to WHMCS.
    :param url: String, base url for whmcs requests
    :param parameters: Dictionary, payload to send to whmcs
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    :raises WhmcsConnectionError: If the network request fails.
    """
    try:
        return requests.post(url=url, data=parameters)
    except RequestException:
        raise WhmcsConnectionError("Could not reach whmcs server.")


def get_response_data(response):
    """
    Get data from a network response.
    :param response: requests.Response, the network response.
    :return: :Dictionary or None: the data from the network response if able to deserialize response json data,
        Otherwise, None
    """
    try:
        return response.json()
    except ValueError:
        return None


def get_error_message(whmcs_response_data):
    """
    Extract an error message from whmcs response data.
    :param whmcs_response_data: Dictionary. The data received from whmcs from which to extract the message.
    :return: :String or None: The error message in the whmcs response data or None if none
    """
    if whmcs_response_data:
        result = whmcs_response_data.get('result', None)
        error = whmcs_response_data.get('message', None)
        if result == "error":
            return error
    return None

# class WhmcsApi:
#     def get_whmcs_response(self, parameters) -> (dict, str):
#         parameters.update(self.get_whmcs_secrets())
#         network = NetworkRequests(base_url="www.olitt.com", force_ssl=True)
#         try:
#             response = network.post_form_data_request("/billing/includes/api.php", parameters, {})
#         except OlittNetworkingException as e:
#             raise APIException(detail="WHMCS Connection Error: {}".format(e.message))
#         else:
#             if response.get('result', 'error') == "success":
#                 return response, None
#             return None, response.get('message', None)
#
#
# class WhmcsProductsApi(WhmcsApi):
#     default_affiliate_enroll_error = "We were unable to enroll you for affiliate"
#     default_affiliate_retrieve_error = "We were unable to retrieve your for affiliate details"
#     default_affiliate_retrieve_all_error = "We were unable to retrieve affiliate details"
#
#     def enroll_affiliate(self, billing_account_id: int) -> bool:
#         parameters = {
#             'action': 'AffiliateActivate',
#             'userid': str(billing_account_id)
#         }
#         whmcs_response, error = self.get_whmcs_response(parameters)
#         if whmcs_response:
#             return True
#         raise APIException(detail=self.default_affiliate_enroll_error if error is None else error)
#
#     def get_affiliate(self, billing_account_id: int) -> Affiliate:
#         affiliates = self.get_affiliates(billing_account_id)
#         if affiliates:
#             return affiliates[0]
#         raise APIException(detail=self.default_affiliate_retrieve_error)
#
#     def get_affiliates(self, billing_account_id: int = 0) -> list:
#         parameters = {'action': 'GetAffiliates'}
#         if billing_account_id != 0:
#             parameters.update({'userid': str(billing_account_id)})
#         whmcs_affiliates, error = self.get_whmcs_response(parameters)
#         if whmcs_affiliates:
#             return deserialize_whmcs_affiliates(whmcs_affiliates)
#         raise APIException(detail=self.default_affiliate_retrieve_all_error if error is None else error)
