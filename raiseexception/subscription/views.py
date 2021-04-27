from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from raiseexception import settings
from raiseexception.mailing.client import MailClient
from raiseexception.mailing.models import To
from raiseexception.subscription.models import Subscription


async def subscribe_view(request: Request):
    status_code = 200
    message = ''
    if request.method == 'POST':
        status_code = 400
        data = await request.form()
        email = data.get('email')
        message = 'email is required'
        if email:
            name = data.get('name')
            await Subscription.create(
                name=name,
                email=data.get('email')
            )
            mail_client = MailClient()
            await mail_client.send(
                to=To(name=name, email=email),
                subject='Subscription',
                message=f'Hi {name}, thanks for subscribing. Click '
                        f'<a href="{settings.SITE}/subscription/verify">here'
                        '</a> to verify your email.'
            )
            status_code = 201
            message = 'Subscription created. I sent you a email to verify it.'
    return settings.TEMPLATE.TemplateResponse(
        name='/subscription/subscribe.html',
        status_code=status_code,
        context={'request': request, 'message': message}
    )


routes = (
    Route('/', subscribe_view, methods=['GET', 'POST']),
)

subscription_views = Starlette(routes=routes)
