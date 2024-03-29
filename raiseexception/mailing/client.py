import httpx

from .models import To
from raiseexception import settings


class MailClient:
    _base_url = 'https://api.mailjet.com/v3.1'
    _username = settings.MAIL_USERNAME
    _password = settings.MAIL_PASSWORD
    _sand_box = settings.MAIL_SANDBOX

    async def send(self, to: To, subject: str, message: str):
        async with httpx.AsyncClient(auth=(self._username, self._password)) \
                as client:
            response = await client.post(
                url=f'{self._base_url}/send',
                headers={'Content-Type': 'application/json'},
                json={
                    'SandboxMode': self._sand_box,
                    'Messages': [
                        {
                            'From': {
                                'Email': 'no-reply@raiseexception.dev',
                                'Name': 'RaiseException'
                            },
                            'To': [
                                {
                                    'Email': to.email,
                                    'Name': to.name
                                }
                            ],
                            'Subject': subject,
                            'HTMLPart': message
                        }
                    ]
                }
            )
        return not response.is_error
