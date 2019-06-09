# services/place/project/tests/utils.py
from project import db
from project.api.models import Place


def add_place(name):
    place = Place(
        name=name
    )
    db.session.add(place)
    db.session.commit()
    return place