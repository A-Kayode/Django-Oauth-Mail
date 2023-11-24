from django.conf import settings

# https://outlook.office.com/.default
# https://graph.microsoft.com/.default
# https://outlook.office.com/SMTP.SendAsApp
AZURE_OAUTH_SCOPES = ["https://graph.microsoft.com/.default"]

AZURE_TENANT = f"https://login.microsoftonline.com/{settings.DJANGO_OAUTH_MAIL_SETTINGS['OUTLOOK']['azure_tenant_name']}"