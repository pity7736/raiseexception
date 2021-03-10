from kinton import Model, fields


class User(Model):
    username = fields.CharField()
    email = fields.CharField()
    password = fields.CharField()
