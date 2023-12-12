from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer, EntitiesRequestAddSerializer
from glados.repositories.entities import get_entities
from glados.models import Entity
from glados import db

class EntitiesAPI(Resource):
    def get(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.args)

        entities = get_entities(data)

        serializer = EntityResponseSerializer(many=True)
        return serializer.dump(entities), 200

    def put(self, id):
        request_serializer = EntitiesRequestAddSerializer()
        data = request_serializer.load(request.get_json())
        errors = request_serializer.validate(data)
        if errors:
            return {"errors": errors}, 400

        entity_id = data.get("id")

        if entity_id is None:
            return {"error": "Entity ID is required for updating an entity"}, 400

        entity = Entity.query.get(entity_id)

        modifications = data.get("modifications", {})

        if "name" in modifications:
            entity.name = modifications["name"]

        if "type" in modifications:
            entity.type = modifications["type"]

        if "status" in modifications:
            entity.status = modifications["status"]

        db.session.commit()
        serializer = EntityResponseSerializer()

        return serializer.dump(entity), 200
