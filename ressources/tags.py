import uuid
from pyexpat.errors import messages

from flask import Flask, request, session
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import  TagSchema, TagAndItemSchema

blp = Blueprint("Tags", __name__, description = "Operations on Tags")

schema_tag = TagSchema()
schemas_tag = TagSchema(many=True)

@blp.route("/tags/<string:tag_id>")
class Tags(MethodView):
    def get(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return schema_tag.dump(tag)

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it",
        example={"message" : "Tag deleted."}
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message" : "Tag deleted"}
        abort(400, message="Couldn't delete Tag")


@blp.route("/store/<string:store_id>/tags")
class tagsList(MethodView):

    def get(self,store_id):
        store = StoreModel.query.get(store_id)
        tags = store.tags
        return schemas_tag.dump(tags)
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self,tag_data,store_id):
        tag = TagModel(store_id = store_id, **tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, message = "couldn't add the tag in the DB")
        return tag

@blp.route("/item/<string:item_id>/tags/<string:tag_id>")
class LinkTagsToItems(MethodView):
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = ItemModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(500, message = "An error occurred while nserting the tag.")
        return tag

    @blp.response(201, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = ItemModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(500, message = "An error occurred while nserting the tag.")
        return {"message" : "Item removed from tag", "item" : item, "tag": tag}
