# services/places/project/api/models.py

from project import db


class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "# Place ID:{} - {}".format(self.id, self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }
