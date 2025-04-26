from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

# Initialize extensions 
db = SQLAlchemy()      
jwt = JWTManager()       
migrate = Migrate()       

# Application Factory Pattern
def create_app():
    app = Flask(__name__)  
    app.config.from_object(Config)  

    # Initialize extensions with the app
    db.init_app(app)       
    jwt.init_app(app)      
    CORS(app)            
    migrate.init_app(app, db)  

    # Register Blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)  

    return app  