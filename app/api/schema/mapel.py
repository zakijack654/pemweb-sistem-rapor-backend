from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from api.models import Mapel
from .jurusan import JurusanSchema
from api import db

class MapelSchema(SQLAlchemySchema):
    class Meta:
        model = Mapel
        sqla_session = db.session
        load_instance = True
    
    id_mapel = auto_field()
    nama_mapel = auto_field()
    jurusan = Nested(JurusanSchema, only=['nama_jurusan'], dump_only=True)
    id_jurusan = auto_field(load_only=True)
    reg_date = auto_field(dump_only=True)