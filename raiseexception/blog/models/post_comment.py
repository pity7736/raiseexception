import re

from kinton import Model, fields

from .post import Post
from ..constants import PostCommentState


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
            if '@' not in value:
                raise ValueError('wrong email')

            user_regex = re.compile(
                r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`"
                r"{}|~0-9A-Z]+)*\Z"
                r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # noqa: E501
                re.IGNORECASE
            )
            domain_regex = re.compile(
                r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',  # noqa: E501
                re.IGNORECASE
            )
            user, domain = value.rsplit('@', 1)
            if not user_regex.match(user) or not domain_regex.match(domain):
                raise ValueError('wrong email')
        self._email = value
