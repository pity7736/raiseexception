from pytest import mark

from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To


@mark.asyncio
async def test_success():
    client = MailClient()
    result = await client.send(
        to=To(email='pity7736@github.com', name='test'),
        message='this is the email content'
    )
    assert result is True
