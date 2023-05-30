import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from raiseexception import settings
from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To
from raiseexception.subscription.models import Subscription
from raiseexception.utils.crypto import get_random_string


def validate_captcha(f):
    async def _validate(request: Request):
        if request.method == 'POST':
            data = await request.form()
            if settings.DEBUG is False:
                captcha_token = data.get('h-captcha-response')
                if captcha_token:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            url='https://hcaptcha.com/siteverify',
                            headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            data={'response': captcha_token, 'secret': settings.HCAPTCHA_SECRET}
                        )
                        response_data = response.json()
                        if response_data['success'] is True:
                            return await f(request)

            return settings.TEMPLATE.TemplateResponse(
                name='/subscription/subscribe.html',
                status_code=400,
                context={'request': request, 'message': 'error validando captcha'}
            )
        return await f(request)
    return _validate


@validate_captcha
async def subscribe_view(request: Request):
    status_code = 200
    message = ''
    if request.method == 'POST':
        status_code = 400
        data = await request.form()
        email = data.get('email')
        message = 'email is required'
        if email:
            subscription = await Subscription.get_or_none(email=email)
            message = 'the email was already subscribed'
            if not subscription:
                name = data.get('name') or None
                token = get_random_string(length=100)
                # TODO: nyoibo - refactor this with entity validations
                try:
                    await Subscription.create(
                        name=name,
                        email=data.get('email'),
                        token=token
                    )
                except ValueError:
                    status_code = 400
                    message = 'invalid email'
                else:
                    mail_client = MailClient()
                    await mail_client.send(
                        to=To(name=name, email=email),
                        subject='Subscription',
                        message=f'Hi {name}, thanks for subscribing. Click '
                                f'<a href="{settings.SITE}/subscription/verify'
                                f'?token={token}">here</a> to verify your '
                                f'email.'
                    )
                    status_code = 201
                    message = 'Subscription created. I sent you a email to ' \
                              'verify it.'
    return settings.TEMPLATE.TemplateResponse(
        name='/subscription/subscribe.html',
        status_code=status_code,
        context={'request': request, 'message': message, 'debug': settings.DEBUG}
    )


async def verify_email_view(request: Request):
    subscription = await Subscription.get_or_none(
        token=request.query_params.get('token')
    )
    status_code = 400
    message = 'invalid token'
    if subscription:
        subscription.verified = True
        subscription.token = None
        await subscription.save(
            update_fields=('verified', 'token', 'modified_at')
        )
        status_code = 200
        message = 'email verified successfully'
    return settings.TEMPLATE.TemplateResponse(
        name='/subscription/verify_email.html',
        status_code=status_code,
        context={'request': request, 'message': message}
    )


routes = (
    Route('/', subscribe_view, methods=['GET', 'POST']),
    Route('/verify', verify_email_view)
)

subscription_views = Starlette(routes=routes)
