from flask import request
from flask_restful import Resource

from glados.api.entity.serializers import EntitiesRequestSerializer, EntityResponseSerializer
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

    def put(self):
        request_serializer = EntitiesRequestSerializer()
        data = request_serializer.load(request.get_json())
        errors = request_serializer.validate(data)

        if errors:
            return {"errors": errors}, 400

        entity_id = data.get("id")

        if entity_id is None:
            return {"error": "Entity ID is required for updating an entity"}, 400

        entity = Entity.query.get(entity_id)

        if entity is None:
            return {"error": "Entity not found"}, 404

        if "name" in data:
            entity.name = data["name"]

        if "type" in data:
            entity.type = data["type"]

        if "status" in data:
            entity.status = data["status"]

        db.session.commit()
        serializer = EntityResponseSerializer()

        return serializer.dump(entity), 200
