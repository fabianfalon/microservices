# services/scores/project/tests/utils.py
from project import db
from project.api.models import People


def add_people(name, isAlive, place_id):
    people = People(
        name=name,
        isAlive=isAlive,
        placeId=place_id
    )
    db.session.add(people)
    db.session.commit()
    return people
