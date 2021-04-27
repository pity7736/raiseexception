import re

from kinton import Model, fields

from .extra_fields import BooleanField


class Subscription(Model):
    _id = fields.IntegerField()
    _name = fields.CharField(default_value='anonymous')
    _email = fields.CharField()
    _verified = BooleanField(default_value=False)
    _token = fields.CharField()
    _created_at = fields.DatetimeField(auto_now_add=True)
    _modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'

    def set_email(self, value):
        value = Subscription._email.parse(value).lower()
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
