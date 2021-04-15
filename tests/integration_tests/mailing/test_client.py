from pytest import mark

from raiseexception import settings
from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To


@mark.asyncio
async def test_success():
    client = MailClient()
    result = await client.send(
        to=To(email=settings.ADMIN_EMAIL, name='test'),
        subject='test email',
        message='this is the email content'
    )
    assert result is True
