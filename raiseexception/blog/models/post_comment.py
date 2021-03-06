from kinton import Model, fields

from raiseexception.blog.constants import PostCommentState
from raiseexception.utils.validate_email import validate_email
from .post import Post


class PostComment(Model):
    _id = fields.IntegerField()
    _post = fields.ForeignKeyField(to=Post)
    _name = fields.CharField(default_value='anonymous')
    _email = fields.CharField()
    _state = fields.CharField(
        choices=PostCommentState,
        default_value=PostCommentState.PENDING
    )
    _body = fields.CharField()
    _created_at = fields.DatetimeField(auto_now_add=True)
    _modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        db_table = 'post_comments'

    async def _insert(self):
        # TODO: fix this in kinton
        state = self._state
        self._state = state.value
        await super()._insert()
        self._state = state

    async def _update(self, update_fields=()):
        # TODO: fix this in kinton
        state = self._state
        self._state = state.value
        await super()._update(update_fields)
        self._state = state

    def set_email(self, value):
        value = PostComment._email.parse(value)
        if value:
            validate_email(value)
        self._email = value
