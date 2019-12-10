from src import db


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

    def save(self, commit=True):
        """ save """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, payload, commit=True):
        for attr, value in payload.items():
            setattr(self, attr, value)
        return commit and self.save() or self
