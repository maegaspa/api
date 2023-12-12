from marshmallow import fields, validate

from glados import ma, constants
from glados.models import Entity

class EntitiesRequestSerializer(ma.Schema):
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    room = fields.String(required=False, validate=validate.OneOf(["Bedroom", "Bathroom", "Living Room", "Kitchen"]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))

class EntitiesRequestAddSerializer(ma.Schema):
    id = fields.UUID(required=True)
    modifications = fields.Dict(required=True)
    type = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityType]))
    room = fields.String(required=False, validate=validate.OneOf(["Bedroom", "Bathroom", "Living Room", "Kitchen"]))
    status = fields.String(required=False, validate=validate.OneOf([x.name for x in constants.EntityStatus]))

class EntitySerializer(ma.Schema):
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Entity
        ordered = True
        fields = [
            "id",
            "name",
            "type",
            "status",
            "value",
            "created_at"
        ]


class EntityResponseSerializer(EntitySerializer):
    pass
