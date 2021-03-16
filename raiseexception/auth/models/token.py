from kinton import Model, fields

from raiseexception.accounts.models import User


class Token(Model):
    _id = fields.IntegerField()
    _value = fields.CharField()
    _user = fields.ForeignKeyField(to=User)

    class Meta:
        db_table = 'tokens'
