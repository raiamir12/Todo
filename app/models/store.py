"""Store Model"""
from app.db import db


class StoreModel(db.Model):
    """Store Model Class"""
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        """Return Response In JSON Format"""
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        """Get Record By Name"""
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """Save Data """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete Data"""
        db.session.delete(self)
        db.session.commit()
