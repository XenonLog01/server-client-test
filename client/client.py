"""
client.py

Author: Xenon

A basic client which can sent POST and GET requests.

Functions:
 - req_Post :: None : Sends a POST request to the server at the specified address.
 - req_Get :: None : Sends a GET request to the server at the specified address.
"""

from helpers.util import *
import requests
import dotenv
import os

dotenv.load_dotenv()

port = int(os.getenv('PORT'))  # The localhost port I'm using for testing.

@debug_time
def req_Post(server: str, data: dict):
    """ Sends a POST request to the specified address, and then reports
    back with the status of the request.

    Parameters:
     - server :: str : The address of the server to send the request to.
     - database :: dict : The database to send in the header of the request.

    Returns :: None
    """
    print(f'{INFO_DEBUG}Sending POST request..')
    try:
        response = requests.post(server, json=data)  # Send a POST request.
        print(
            f"{INFO_RESULT}POST was a "
            f"{f'{TEXT_GREEN}success{TEXT_RESET}.' if response.status_code == 200 else f'{TEXT_RED}failure{TEXT_RESET}, with error code {TEXT_CYAN}{response.status_code}{TEXT_RESET}.'}"
        )
    except requests.exceptions.ConnectionError:
        # If the server never responds, thrown an error.
        print(f"{INFO_ERROR} Server is unable to be reached!")

@debug_time
def req_Get(server: str, data: dict):
    """ Sends a GET request to the specified address, and then reports
    back with the status of the request.

    Parameters:
     - server :: str : The address of the server to send the request to.
     - database :: dict : The database to send in the header of the request.

    Returns :: None
    """
    print(f"{INFO_DEBUG}Sending GET request..")
    try:
        response = requests.get(server, json=data)  # Send a GET request.
        print(
            f"{INFO_RESULT}GET request was a "
            f"{f'{TEXT_GREEN}success{TEXT_RESET}.' if response.status_code == 200 else f'{TEXT_RED}failure{TEXT_RESET}, with error code {TEXT_CYAN}{response.status_code}{TEXT_RESET}.'}"
        )
        print(f"{INFO_RESULT}Response was: {TEXT_L_GREY}{response.text}{TEXT_RESET}")
    except requests.exceptions.ConnectionError:
        # If the server never responds, thrown an error.
        print(f"{INFO_ERROR} Server is unable to be reached!")

if __name__ == '__main__':
    # req_Post(f'http://localhost:{port}/', {'id': 1})
    req_Get(f'http://localhost:{port}/', {'id': 0})
