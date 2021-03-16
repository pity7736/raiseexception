from kinton import Model, fields

from raiseexception.utils.crypto import make_password


class User(Model):
    _id = fields.IntegerField()
    _username = fields.CharField()
    _email = fields.CharField()
    _password = fields.CharField()

    class Meta:
        db_table = 'users'

    def set_password(self, value: str):
        if self._id is None:
            self._password = make_password(value)
        else:
            self._password = value

    def get_password_salt(self):
        return self._password.split('$')[0]
