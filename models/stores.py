from db import db


class Store(db.Model):
    __tablename__ = "Store"
    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    items = db.relationship("Item", back_populates="store", lazy="dynamic",  cascade="all, delete")
    tags = db.relationship("Tag", back_populates="store", lazy="dynamic", cascade="all, delete")