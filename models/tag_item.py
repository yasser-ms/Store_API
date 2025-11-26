from db import db

class TagItem(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("Item.item_id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))


    item = db.relationship("Item", back_populates="tags_links")
    tag = db.relationship("Tag", back_populates="items_links")