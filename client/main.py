from debug import *
import requests
import dotenv
import json
import os

dotenv.load_dotenv()

port = int(os.getenv('PORT'))

data = {
    'id': 1,
}

# Send POST request, and report the status.
@debug_time
def req_Post(msg: dict):
    print(f'{INFO_DEBUG}Sending POST request..')
    try:
        response = requests.post(f'http://localhost:{port}/', json=msg)
        print(
            f"{INFO_RESULT}POST was a "
            f"{f'{TEXT_GREEN}success{TEXT_RESET}.' if response.status_code == 200 else f'{TEXT_RED}failure{TEXT_RESET}, with error code {TEXT_CYAN}{response.status_code}{TEXT_RESET}.'}"
        )
    except requests.exceptions.ConnectionError:
        print(f"{INFO_ERROR} Server is unable to be reached!")

@debug_time
def req_Get():
    print(f"{INFO_DEBUG}Sending GET request..")
    try:
        response = requests.get(f'http://localhost:{port}/', json={'id': 0})
        # print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
        print(
            f"{INFO_RESULT}GET request was a "
            f"{f'{TEXT_GREEN}success{TEXT_RESET}.' if response.status_code == 200 else f'{TEXT_RED}failure{TEXT_RESET}, with error code {TEXT_CYAN}{response.status_code}{TEXT_RESET}.'}"
        )
    except requests.exceptions.ConnectionError:
        print(f"{INFO_ERROR} Server is unable to be reached!")

def main():
    # req_Post(data)
    req_Get()

if __name__ == '__main__':
    main()
