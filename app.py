import uuid
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt
)
import secrets
from flask_smorest import Api

from flask_migrate import migrate, Migrate
from db import db
from BlockList import BLOCKLIST,is_token_revoked, add_token_to_blocklist, remove_token_from_blocklist
from ressources.items import blp as ItemsBleuPrint
from ressources.stores import blp as StoresBleuPrint
from ressources.tags import blp as tagsBleuprint
from ressources.user import blp as userBleuprint

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        add_token_to_blocklist("test-jti")
        revoked = is_token_revoked("test-jti")
        return f"Token revoked? {revoked}"

    # Flask-Smorest config
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'My Flask-Smorest API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # SQLAlchemy config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    from models.user import User as UserModel
    from models.items import Item as ItemModel
    from models.stores import Store as StoreModel
    from models.tags import Tag as TagModel
    from models.tag_item import TagItem as TagItemModel
    migrate = Migrate(app, db)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = "268244294231956291204044849880971025459"
    jwt = JWTManager(app)

    # Blocklist loader
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return is_token_revoked(jti)  # Returns True if token is revoked

    # custom response when a revoked token is used
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has been revoked"}), 401

    # Register Blueprints
    api.register_blueprint(StoresBleuPrint)
    api.register_blueprint(ItemsBleuPrint)
    api.register_blueprint(tagsBleuprint)
    api.register_blueprint(userBleuprint)

    # Create tables once at startup
  ##  with app.app_context():
    ##    db.create_all()

    return app
