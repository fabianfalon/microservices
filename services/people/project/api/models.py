# services/people/project/api/models.py

from project import db


class PeopleException(Exception):
    pass


class People(db.Model):
    __tablename__ = 'peoples'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    isAlive = db.Column(db.Boolean, nullable=True)
    isKing = db.Column(db.Boolean, nullable=True, default=False)
    placeId = db.Column(db.Integer)

    def __init__(self, name, isAlive, placeId):
        self.name = name
        self.isAlive = isAlive
        self.placeId = placeId

    def __repr__(self):
        return "#Person ID:{} - {}".format(self.id, self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'isAlive': self.isAlive,
            'placeId': self.placeId,
            'isKing': self.isKing
        }

    def save(self, commit=True):
        """ save people"""
        if self.isKing and self.query.filter_by(isKing=True).count() == 1:
            raise PeopleException(
                "The person could not be saved, because a king already exists in this place"
            )
        else:
            db.session.add(self)
            if commit:
                db.session.commit()
            return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()
