from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256 ## algorithm to hash the password
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import UserModel
from schemas import UserSchema
from BlockList import BLOCKLIST


blp = Blueprint("Users", "users", description = "Operations on users")


@blp.route("/register")
class userRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message = "A user with that username already exists." )

        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError :
            abort(400, message = "coudln't store the user")
        return {"message" : "user created ! "}, 201

@blp.route("/login")
class UserLOgin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity= str(user.id), fresh=True)
            refresh_tocken = create_refresh_token(identity= str(user.id))

            return {"access_token" : access_token, "refresh token" : refresh_tocken}
        abort(401, message ="Invalid credentials")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message" : "User deleted."}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"] ## get jti
        BLOCKLIST.add(jti)
        return {"message" : "Successfully logged out"}

@blp.route("/refresh")
class UserRefresh(MethodView):
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_access_token,
        "msg": "Access token refreshed successfully"}, 201