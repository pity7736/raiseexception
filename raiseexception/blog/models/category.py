from kinton import Model, fields


class Category(Model):
    _id = fields.IntegerField()
    _name = fields.CharField()

    class Meta:
        db_table = 'categories'
