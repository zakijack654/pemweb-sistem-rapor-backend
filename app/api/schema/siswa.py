from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from api.models import Siswa
from .kelas import KelasSchema
from api import db

class SiswaSchema(SQLAlchemySchema):
    class Meta:
        model = Siswa
        sqla_session = db.session
        load_instance = True
    
    nis = auto_field()
    nama_siswa = auto_field()
    email = auto_field()
    jenkel = auto_field()
    kelas = Nested(KelasSchema, only=["jenjang_kelas", "urutan_kelas", "jurusan"], dump_only=True)
    id_kelas = auto_field(load_only=True)
    isActive = auto_field()
    reg_date = auto_field(dump_only=True)