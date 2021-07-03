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
    from .routes.jurusan import jurusan
    from .routes.mapel import mapel
    from .routes.periode_ajaran import periode_ajaran
    app.register_blueprint(siswa, url_prefix='/api')
    app.register_blueprint(jurusan, url_prefix='/api')
    app.register_blueprint(mapel, url_prefix='/api')
    app.register_blueprint(periode_ajaran, url_prefix='/api')

    return app