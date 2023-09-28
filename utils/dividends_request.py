import json
import logging
import requests
from fastapi import status
from settings import settings
from generate_auth_token import get_auth_token
url_host = f'http://{settings.API.LOCALHOST}:{settings.API.LOCAL_PORT}/api/v1/dividends'


logger = logging.getLogger(__name__)


def create_dividend(request_body):
    auth_token = get_auth_token()
    if auth_token:
        payload = json.dumps(request_body)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }
        response = requests.request("POST", url_host, headers=headers, data=payload)
        if response.status_code == status.HTTP_200_OK:
            return True
        else:
            logger.exception(response.text)
            logger.exception(f"Status returned by POST request is other than 200. It is: {response.status_code}")
    else:
        logger.exception("Auth token couldn't be generated.")
    return False


if __name__ == '__main__':
    create_dividend({})
