import inspect

import factory
from kinton import Model

from raiseexception.accounts.models import User
from raiseexception.blog.models import Category, Post, PostComment
from raiseexception.subscription.models import Subscription


class AsyncFactory(factory.Factory):

    @classmethod
    def _create(cls, model_class: Model, **kwargs):
        async def create():
            for key, value in kwargs.copy().items():
                if inspect.isawaitable(value):
                    kwargs[key] = await value
            return await model_class.create(**kwargs)
        return create()

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class UserFactory(AsyncFactory):
    username = '__pity__'
    email = factory.Sequence(lambda n: f'user{n}@email.com')
    password = 'test password'

    class Meta:
        model = User


class CategoryFactory(AsyncFactory):
    name = factory.Faker('name')

    class Meta:
        model = Category


class PostFactory(AsyncFactory):
    title = factory.Faker('sentence')
    body = factory.Faker('paragraph')
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    description = factory.Faker('sentence')

    class Meta:
        model = Post


class PostCommentFactory(AsyncFactory):
    name = factory.Faker('name')
    post = factory.SubFactory(PostFactory)
    email = 'anonymous@pm.me'
    body = factory.Faker('paragraph')

    class Meta:
        model = PostComment


class SubscriptionFactory(AsyncFactory):
    name = factory.Faker('name')
    email = factory.Faker('email')
    verified = False

    class Meta:
        model = Subscription
