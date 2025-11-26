from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import ItemModel
from schemas import ItemUpdateSchema, ItemSchema

blp = Blueprint("Items", __name__, description = "Operations on items")

shema_item = ItemSchema()
schema_item = ItemSchema(many=True)

@blp.route("/item/<string:item_id>")

class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id = item_id, **item_data)
            db.session.add(item)
        db.session.commit()
        return item

    @jwt_required()
    @blp.response(200, ItemSchema)
    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, message = "couldn't delete the item")
        return {"massage" : "item deleted"}

@blp.route("/item")
class ItemsList(MethodView):
    def get(self):
        items =  ItemModel.query.all()
        return schema_item.dump(items)

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "there was an error while inserting the item")
        return item