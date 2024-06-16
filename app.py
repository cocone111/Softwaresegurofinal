from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supermercado.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from routes import auth_blueprint, inventory_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(inventory_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
