from nyoibo import fields
from nyoibo.entities.entity import Entity


class To(Entity):
    _email = fields.StrField()
    _name = fields.StrField()
