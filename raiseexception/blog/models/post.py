from kinton import Model, fields

from raiseexception.blog.models.category import Category


class Post(Model):
    _id = fields.IntegerField()
    _title = fields.CharField()
    _body = fields.CharField()
    _category = fields.ForeignKeyField(to=Category)

    class Meta:
        db_table = 'posts'
