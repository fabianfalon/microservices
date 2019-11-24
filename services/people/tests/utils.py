from src import db
from src.models.people import People


def add_people(name, isAlive, place_id):
    people = People(
        name=name,
        isAlive=isAlive,
        placeId=place_id
    )
    db.session.add(people)
    db.session.commit()
    return people
