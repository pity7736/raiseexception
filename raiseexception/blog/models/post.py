import re
import unicodedata

from kinton import Model, fields

from raiseexception.accounts.models import User
from raiseexception.blog.constants import PostState
from raiseexception.blog.models.category import Category


class Post(Model):
    _id = fields.IntegerField()
    _title = fields.CharField()
    _title_slug = fields.CharField(immutable=True)
    _body = fields.CharField()
    _state = fields.CharField(choices=PostState, default_value=PostState.DRAFT)
    _category = fields.ForeignKeyField(to=Category)
    _author = fields.ForeignKeyField(to=User)
    _created_at = fields.DatetimeField(auto_now_add=True)
    _modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        db_table = 'posts'

    def set_title(self, value):
        value = str(value)
        self._title = value
        value = unicodedata.normalize(
            'NFKD',
            value
        ).encode(
            'ascii',
            'ignore'
        ).decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        self._title_slug = re.sub(r'[-\s]+', '-', value).strip('-_')

    async def _insert(self):
        # TODO: fix this in kinton
        state = self._state
        self._state = state.value
        await super()._insert()
        self._state = state
