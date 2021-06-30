from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Create app and basic configs here (DB, etc.)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/sistem_rapor_pweb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # initialize the database
    
    db.init_app(app)
    
    # Register blueprints
    from .routes.siswa import siswa
    app.register_blueprint(siswa, url_prefix='/api')

    return app