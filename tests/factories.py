import factory

from raiseexception.accounts.models import User
from raiseexception.blog.models import Category


class AwaitableFactoryMixin:

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create():
            return await model_class.create(*args, **kwargs)
        return create()

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class UserFactory(AwaitableFactoryMixin, factory.Factory):
    username = '__pity__'
    email = 'test@email.com'
    password = 'test password'

    class Meta:
        model = User


class CategoryFactory(AwaitableFactoryMixin, factory.Factory):
    name = factory.Faker('name')

    class Meta:
        model = Category
