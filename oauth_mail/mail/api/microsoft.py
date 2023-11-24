import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

from oauth_mail.security.azure import AzureSecurityToken


class GraphAPIMailBackend(BaseEmailBackend):
    def __init__(self, host=None, save_sent_message=False, fail_silently=False, **kwargs):
        self.host = settings.EMAIL_HOST_USER if host is None else host
        self.save_sent_message = save_sent_message
        super().__init__(fail_silently=fail_silently)

    def send_messages(self, email_messages):
        """Method used to send messages and return the number of email messages sent"""
        if not email_messages:
            return 0

        messages_sent = 0
        token = AzureSecurityToken.get_token()
        headers = {"Content-Type":"application/json", "Authorization":f"Bearer {token}"}
        for message in email_messages:
            payload = {
                "message": {
                    "subject": message.subject,
                    "body": {
                        "content": message.body,
                        "contentType": message.content_subtype if message.content_subtype == "html" else "text",
                    },
                    "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in message.to],
                    "bccRecipients": [{"emailAddress": {"address": bcc}} for bcc in message.bcc]
                },
                "saveToSentItems": self.save_sent_message
            }
            response = requests.post(f"https://graph.microsoft.com/v1.0/users/{self.host}/sendMail", json=payload, headers=headers)
            if response.status_code == 202:
                messages_sent = messages_sent + 1
        
        return messages_sent
            
        
        




def test_mail():
    token = AzureSecurityToken.get_token()
    if token:
        headers = {"Content-Type":"application/json", "Authorization":f"Bearer {token}"}
        payload = {
            "message": {
                "subject": "Testing Graph Mail",
                "body": {"content":"This is the content of the message being sent for the test", "contentType":"text"},
                "toRecipients": [
                    {"emailAddress": {"address":"don.kayode@yahoo.com"}}        
                ],
            },
            "saveToSentItems": False
        }

        res = requests.post(f"https://graph.microsoft.com/v1.0/users/{settings.EMAIL_HOST_USER}/sendMail", json=payload, headers=headers)
        print(res.status_code)
        print(type(res.status_code))
        print(res.text)