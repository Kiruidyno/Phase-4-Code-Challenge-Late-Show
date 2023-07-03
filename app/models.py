from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm.exc import NoResultFound


db = SQLAlchemy()

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vendor_sweets = relationship('VendorSweet', back_populates='vendor')

class Sweet(db.Model):
    __tablename__ = 'sweet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vendor_sweets = relationship('VendorSweet', back_populates='sweet')

class VendorSweet(db.Model):
    __tablename__ = 'vendor_sweet'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweet.id'), nullable=False)
    vendor = db.relationship('Vendor', back_populates='vendor_sweets')
    sweet = db.relationship('Sweet', back_populates='vendor_sweets')

    @classmethod
    def get_by_id(cls, vendor_sweet_id):
        try:
            return cls.query.filter_by(id=vendor_sweet_id).one()
        except NoResultFound:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.sweet.name,
            'price': self.price
        }

    @staticmethod
    def validate_price(context):
        if context.is_insert:
            if context.current_parameters['price'] is None:
                raise ValueError('Price cannot be blank.')
            if context.current_parameters['price'] < 0:
                raise ValueError('Price cannot be a negative number.')

db.event.listen(VendorSweet.price, 'set', VendorSweet.validate_price)
