from kinton import Model, fields
from kinton.db_client import DBClient

from raiseexception.accounts.models import User


class Token(Model):
    _id = fields.IntegerField()
    _value = fields.CharField()
    _user = fields.ForeignKeyField(to=User)

    class Meta:
        db_table = 'tokens'

    async def delete(self):
        # TODO: refactor this in kinton
        db_client = DBClient()
        await db_client.update('DELETE FROM tokens WHERE id = $1', self.id)
