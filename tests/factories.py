import factory

from raiseexception.accounts.models import User


class AwaitableFactoryMixin:

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create():
            return await model_class.create(*args, **kwargs)
        return create()


class UserFactory(AwaitableFactoryMixin, factory.Factory):
    username = '__pity__'
    email = 'test@email.com'
    password = 'test password'

    class Meta:
        model = User
