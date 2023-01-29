"""Items Model"""
from app.db import db

class ItemModel(db.Model):
    """Item Model Class"""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        """Return Response In JSON Format"""
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        """Get Record By Name"""
        return cls.query.filter_by(name=name).first()  # simple TOP 1 select

    def save_to_db(self):  # Upserting data
        """Save Data In DB"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete Data From DB"""
        db.session.delete(self)
        db.session.commit()
