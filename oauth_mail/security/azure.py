import logging

from django.conf import settings
from msal import ConfidentialClientApplication

from .utils import AZURE_OAUTH_SCOPES, AZURE_TENANT


class AzureSecurityToken:
    def get_token():
        app = ConfidentialClientApplication(client_id=settings.DJANGO_OAUTH_MAIL_SETTINGS['OUTLOOK']['azure_app_client_id'], client_credential=settings.DJANGO_OAUTH_MAIL_SETTINGS['OUTLOOK']['azure_app_client_secret'], authority=AZURE_TENANT)

        result = None
        result = app.acquire_token_silent(scopes=AZURE_OAUTH_SCOPES, account=None)

        if not result:
            logging.info("No suitable token exists in cache. Getting a new one from AAD")
            result = app.acquire_token_for_client(scopes=AZURE_OAUTH_SCOPES)
        
        if "access_token" in result:
            # print(True)
            # print(result['access_token'])
            return result['access_token']
        else:
            # print(result)
            # print("No access token gotten")
            return False