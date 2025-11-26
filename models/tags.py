from db import db


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(88), unique = True, nullable = False)
    store_id = db.Column(db.String(80), db.ForeignKey("Store.store_id", ondelete="CASCADE"), unique = False, nullable = False)
    store = db.relationship("Store", back_populates="tags")
    items_links = db.relationship("TagItem", back_populates = "tag", cascade="all, delete-orphan")
