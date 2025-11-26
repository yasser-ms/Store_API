from db import db


class Item(db.Model):
    __tablename__ = "Item"
    item_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(2), unique=False, nullable=False)
    store_id = db.Column(db.String(80), db.ForeignKey("Store.store_id", ondelete="CASCADE"), unique = False, nullable = False)
    store = db.relationship("Store", back_populates="items")
    tags_links = db.relationship("TagItem", back_populates="item", cascade="all, delete-orphan")