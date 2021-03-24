from kinton import Model, fields

from raiseexception.accounts.models import User
from raiseexception.blog.models.category import Category


class Post(Model):
    _id = fields.IntegerField()
    _title = fields.CharField()
    _body = fields.CharField()
    _category = fields.ForeignKeyField(to=Category)
    _author = fields.ForeignKeyField(to=User)

    class Meta:
        db_table = 'posts'
