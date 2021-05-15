from kinton import Model, fields

from raiseexception.utils.validate_email import validate_email
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
        validate_email(value)
        self._email = value
