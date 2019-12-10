from src import db
from src.models.place import Place


def add_place(name):
    place = Place(
        name=name
    )
    db.session.add(place)
    db.session.commit()
    return place
