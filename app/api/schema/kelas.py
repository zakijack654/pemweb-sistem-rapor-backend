from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from api.models import Kelas
from api import db

class KelasSchema(SQLAlchemySchema):
    class Meta:
        model = Kelas
        sqla_session = db.session
    
    id_kelas = auto_field(dump_only=True)
    jenjang_kelas = auto_field()
    urutan_kelas = auto_field()
    id_jurusan = auto_field()
    wali_kelas = auto_field()