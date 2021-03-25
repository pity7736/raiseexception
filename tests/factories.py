import inspect

import factory

from raiseexception.accounts.models import User
from raiseexception.blog.models import Category, Post


class AwaitableFactoryMixin:

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def create():
            for key, value in kwargs.copy().items():
                if inspect.isawaitable(value):
                    kwargs[key] = await value
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


class PostFactory(AwaitableFactoryMixin, factory.Factory):
    title = factory.Faker('sentence')
    body = factory.Faker('paragraph')
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
