from glados.models import Entity

def get_entities(filters):
    query = Entity.query

    type = filters.get("type")
    if type:
        query = query.filter(Entity.type == type)

    room = filters.get("room")
    if room:
        query = query.join(Entity.room).filter(Entity.room.has(name=room))

    status = filters.get("status")
    if status:
        query = query.filter(Entity.status == status)

    return query.all()
