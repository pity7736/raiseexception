from nyoibo import fields
from nyoibo.entities.entity import Entity


class To(Entity):
    _email = fields.StrField()
    _name = fields.StrField()

    def __eq__(self, other: 'To'):
        return self._email == other._email and self._name == other._name
