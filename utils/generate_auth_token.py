import requests
import logging
from fastapi import status
from settings import settings

url_host = f'http://{settings.API.LOCALHOST}:{settings.API.LOCAL_PORT}/api/v1/auth/token'
logger = logging.getLogger(__name__)


def get_auth_token():
    payload = {
        'email': settings.AUTH.AUTH_EMAIL,
        'password': settings.AUTH.AUTH_PASSWORD
    }

    response = requests.request("POST", url_host, data=payload)

    if response.status_code == status.HTTP_200_OK:
        logger.info(f"Successfully generated auth token for: {settings.AUTH.AUTH_EMAIL}")
        return response.json().get('access_token')
    else:
        logger.exception(f"Couldn't generate access token for: {settings.AUTH.AUTH_EMAIL}")
