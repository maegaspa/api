import uuid
import pytest

from glados import constants
from glados.models import Entity, Room


@pytest.fixture
def entities():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)

    bedroom = Room(id=uuid.UUID(int=3), name="Bedroom")
    bedroom.save(commit=False)

    bathroom = Room(id=uuid.UUID(int=4), name="Bathroom")
    bathroom.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=1),
        name="Ceiling Light",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.off.name,
        value=None,
        room_id=kitchen.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=2),
        name="Lamp",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=200,
        room_id=living_room.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=3),
        name="Thermometer",
        type=constants.EntityType.sensor.name,
        status=constants.EntityStatus.on.name,
        value=28,
        room_id=living_room.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=4),
        name="Switch",
        type=constants.EntityType.switch.name,
        status=constants.EntityStatus.on.name,
        value=1,
        room_id=bedroom.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=5),
        name="Air conditioner",
        type=constants.EntityType.air_conditioner.name,
        status=constants.EntityStatus.on.name,
        value=24,
        room_id=bedroom.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=6),
        name="Bathroom light",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=27,
        room_id=bathroom.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=7),
        name="Bedroom light 1",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.unavailable.name,
        value=56,
        room_id=bedroom.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=8),
        name="switch bathroom",
        type=constants.EntityType.switch.name,
        status=constants.EntityStatus.off.name,
        value=99,
        room_id=bathroom.id)
    entity.save(commit=False)


def test_get_entities_with_invalid_data(client):
    response = client.get("/entities?type=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}
def test_get_entities_with_invalid_filter_room(client):
    response = client.get("/entities?room=Hall")

    assert response.status_code == 422
    assert response.json == {
        "errors": {
            "room": [
                "Must be one of: Bedroom, Bathroom, Living Room, Kitchen."
            ]
        }
    }
def test_get_entities_with_invalid_filter_status(client):
    response = client.get("/entities?status=poff")

    assert response.status_code == 422
    assert response.json == {
        "errors": {
            "status": [
                "Must be one of: on, off, unavailable."
            ]
        }
    }


def test_get_entities(client, entities, mocker):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000004",
            "name": "Switch",
            "type": "switch",
            "status": "on",
            "value": "1",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000005",
            "name": "Air conditioner",
            "type": "air_conditioner",
            "status": "on",
            "value": "24",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000006",
            "name": "Bathroom light",
            "type": "light",
            "status": "on",
            "value": "27",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000007",
            "name": "Bedroom light 1",
            "type": "light",
            "status": "unavailable",
            "value": "56",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000008",
            "name": "switch bathroom",
            "type": "switch",
            "status": "off",
            "value": "99",
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_type_filter(client, entities, mocker):
    response = client.get("/entities?type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        }
    ]

def test_get_entities_with_bathroom_filter(client, entities, mocker):
    response = client.get("/entities?room=Bathroom")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000006",
            "name": "Bathroom light",
            "type": "light",
            "status": "on",
            "value": "27",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000008",
            "name": "switch bathroom",
            "type": "switch",
            "status": "off",
            "value": "99",
            "created_at": mocker.ANY
        }
    ]
def test_get_entities_with_kitchen_filter(client, entities, mocker):
    response = client.get("/entities?room=Kitchen")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        }
    ]

def test_get_entities_with_status_on_filter(client, entities, mocker):
    response = client.get("/entities?status=on")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000004",
            "name": "Switch",
            "type": "switch",
            "status": "on",
            "value": "1",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000005",
            "name": "Air conditioner",
            "type": "air_conditioner",
            "status": "on",
            "value": "24",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000006",
            "name": "Bathroom light",
            "type": "light",
            "status": "on",
            "value": "27",
            "created_at": mocker.ANY
        }
    ]

def test_get_entities_with_status_off_filter(client, entities, mocker):
    response = client.get("/entities?status=off")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000008",
            "name": "switch bathroom",
            "type": "switch",
            "status": "off",
            "value": "99",
            "created_at": mocker.ANY
        }
    ]

def test_get_entities_with_status_unavailable_filter(client, entities, mocker):
    response = client.get("/entities?status=unavailable")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000007",
            "name": "Bedroom light 1",
            "type": "light",
            "status": "unavailable",
            "value": "56",
            "created_at": mocker.ANY
        }
    ]

def test_get_entities_with_type_and_room_filter(client, entities, mocker):
    response = client.get("/entities?type=sensor&room=Living Room")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        }
    ]
def test_get_entities_with_type_and_room_and_status_filter(client, entities, mocker):
    response = client.get("/entities?type=switch&room=Bathroom&status=off")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000008",
            "name": "switch bathroom",
            "type": "switch",
            "status": "off",
            "value": "99",
            "created_at": mocker.ANY
        }
    ]
