from asyncpg import exceptions
from nyoibo import fields
from nyoibo.entities.entity import Entity

from raiseexception.accounts.models import User
from raiseexception.blog.models import Post, Category


class CreatePost(Entity):
    _title = fields.StrField()
    _body = fields.StrField()
    _category_id = fields.StrField()
    _author = fields.LinkField(to=User)
    _description = fields.StrField()

    async def create(self) -> Post:
        self._validate_data()
        await self._resolve_category_id()
        try:
            return await Post.create(
                title=self._title,
                body=self._body,
                category_id=self._category_id,
                author=self._author,
                description=self._description
            )
        except exceptions.ForeignKeyViolationError:
            raise ValueError('does not exists category with id: '
                             f'{self._category_id}')

    def _validate_data(self):
        # TODO: add this validation to nyoibo
        if not self._title:
            raise ValueError('title is obligatory')
        if not self._body:
            raise ValueError('body is obligatory')
        if not self._category_id:
            raise ValueError('category_id is obligatory')
        if not self._author:
            raise ValueError('author is obligatory')
        if not self._description:
            raise ValueError('description is obligatory')

    async def _resolve_category_id(self):
        if self._category_id.isdigit() is False:
            category = await Category.create(name=self._category_id)
            self._category_id = category.id
