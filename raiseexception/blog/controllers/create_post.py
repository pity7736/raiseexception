from asyncpg import exceptions
from nyoibo import fields
from nyoibo.entities.entity import Entity

from raiseexception.blog.models import Post


class CreatePost(Entity):
    _title = fields.StrField()
    _body = fields.StrField()
    _category_id = fields.IntField()

    async def create(self) -> Post:
        self._validate_data()
        try:
            return await Post.create(
                title=self._title,
                body=self._body,
                category_id=self._category_id
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
