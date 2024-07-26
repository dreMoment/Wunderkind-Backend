# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Initialize the Flask app and its configurations
app = Flask(__name__)
app.config.from_pyfile("config.py")  # Change to 'production' as needed

# Initialize Flask extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)

# Register blueprints
from .routes.signup_routes import signup_bp

app.register_blueprint(signup_bp, url_prefix="/")

from .routes.login_routes import login_bp

app.register_blueprint(login_bp, url_prefix="/")

from .routes.parent_routes import parent_bp

app.register_blueprint(parent_bp, url_prefix="/")

from .routes.user_routes import user_bp

app.register_blueprint(user_bp, url_prefix="/")

from .routes.child_routes import child_bp

app.register_blueprint(child_bp, url_prefix="/")

from .routes.task_routes import task_bp

app.register_blueprint(task_bp, url_prefix="/")

from .routes.ml_routes import ml_bp

app.register_blueprint(ml_bp, url_prefix="/")

from .routes.book_routes import book_bp

app.register_blueprint(book_bp, url_prefix="/")

from .routes.question_routes import question_bp

app.register_blueprint(question_bp, url_prefix="/")

from .routes.category_routes import category_bp

app.register_blueprint(category_bp, url_prefix="/")

from .routes.points_routes import points_bp

app.register_blueprint(points_bp, url_prefix="/")

from .routes.reward_routes import reward_bp

app.register_blueprint(reward_bp, url_prefix="/")

from .routes.purchased_rewards_routes import purchased_reward_bp

app.register_blueprint(purchased_reward_bp, url_prefix="/")

from .routes.statistics_routes import statistics_bp

app.register_blueprint(statistics_bp, url_prefix="/")

from .routes.history_routes import history_bp

app.register_blueprint(history_bp, url_prefix="/")


# create a test route
@app.route("/")
def home():
    return "Up and running!"


# Create the SQL tables for our data models
with app.app_context():
    db.create_all()
