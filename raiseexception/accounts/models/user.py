from kinton import Model, fields

from raiseexception import settings
from raiseexception.utils.crypto import make_password


class User(Model):
    _id = fields.IntegerField()
    _username = fields.CharField()
    _email = fields.CharField()
    _password = fields.CharField()

    class Meta:
        db_table = 'users'

    def set_password(self, value: str):
        split_value = value.split('$')
        try:
            unknown_word, salt, password = split_value
            if unknown_word == settings.UNKNOWN_PASSWORD_WORD:
                self._password = f'{salt}${password}'
                return
            raise ValueError()
        except ValueError:
            password = make_password(value)
            self._password = f'{settings.UNKNOWN_PASSWORD_WORD}${password}'
