from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from api.models import PeriodeAjaran
from api import db

class PeriodeAjaranSchema(SQLAlchemySchema):
    class Meta:
        model = PeriodeAjaran
        sqla_session = db.session
        load_instance = True
    
    id = auto_field(dump_only=True)
    tahun_ajaran = auto_field()
    semester = auto_field()