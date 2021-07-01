from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from api.models import Jurusan
from api import db

class JurusanSchema(SQLAlchemySchema):
    class Meta:
        model = Jurusan
        sqla_session = db.session
        load_instance = True
    
    id_jurusan = auto_field()
    nama_jurusan = auto_field()