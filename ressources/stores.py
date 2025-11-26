import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store_schema.dump(store)

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Couldn't delete the store")
        return {"message": "Store deleted successfully"}

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        stores = StoreModel.query.all()
        return {"stores": stores_schema.dump(stores)}

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Store already exists")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Problem inserting the store")
        return store_schema.dump(store)
