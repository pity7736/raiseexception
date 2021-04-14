from pytest import mark

from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To


@mark.asyncio
async def test_success():
    client = MailClient()
    result = await client.send(
        to=To(email='julian.cortes77@pm.me', name='test')
    )
    assert result is True
