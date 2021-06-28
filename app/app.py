from flask import Flask, json, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.ext.automap import automap_base

# DB Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/sistem_rapor_pweb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Automap
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Models / Tables
Siswa = Base.classes.siswa
Kelas = Base.classes.kelas

# -- SCHEMAS --
class KelasSchema(SQLAlchemySchema):
    class Meta:
        model = Kelas
        sqla_session = db.session
    
    id_kelas = auto_field(dump_only=True)
    jenjang_kelas = auto_field()
    urutan_kelas = auto_field()
    id_jurusan = auto_field()
    wali_kelas = auto_field()

class SiswaJoinKelasSchema(SQLAlchemySchema):
    class Meta:
        model = Siswa
        sqla_session = db.session
        load_instance = True
    
    nis = auto_field()
    nama_siswa = auto_field()
    email = auto_field()
    jenkel = auto_field()
    kelas = Nested(KelasSchema, only=["jenjang_kelas", "urutan_kelas", "id_jurusan"])

class SiswaSchema(SQLAlchemySchema):
    class Meta:
        model = Siswa
        sqla_session = db.session
        load_instance = True
    
    nis = auto_field()
    nama_siswa = auto_field()
    email = auto_field()
    jenkel = auto_field()
    id_kelas = auto_field()


# Routes
@app.route('/')
def test():
    return make_response({'message': 'welcome!'}, 200)

@app.route('/siswa', methods=["GET", "POST"])
def get_post_delete_siswa():
    # GET ALL SISWA
    if request.method == "GET":
        all_siswa = db.session.query(Siswa).join(Kelas).all()
        schema = SiswaJoinKelasSchema(many=True)
        result = schema.dump(all_siswa)
        return make_response(jsonify({"siswa": result}), 201)
    # POST SISWA
    elif request.method == "POST":
        params = request.form
        # If siswa already exist, reject request
        if db.session.query(Siswa).get(params['nis']):
            return make_response(jsonify({'error': 'Siswa with this NIS already exist!'}), 404)
        schema = SiswaSchema()
        siswa = schema.load(params)
        db.session.add(siswa)
        db.session.commit()
        result = schema.dump(siswa)
        return make_response(jsonify({'message': 'post success', 'data': result}))

@app.route('/siswa/<nis>', methods=["GET", "DELETE", "PUT"])
def siswa_by_nis(nis):
    # GET ONE SISWA
    if request.method == "GET":
        get_siswa = db.session.query(Siswa).get(nis)
        schema = SiswaJoinKelasSchema()
        result = schema.dump(get_siswa)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)
    # UPDATE ONE SISWA
    if request.method == "PUT":
        params = request.form
        print(params)
        get_siswa = db.session.query(Siswa).get(nis)
        # if siswa doesn't exist, reject request
        if get_siswa is None:
            return make_response(jsonify({'error': 'Siswa not found!'}), 404)
        # Update
        for p in params:
            setattr(get_siswa, p, request.form[p])
        db.session.commit()
        schema = SiswaSchema()
        result = schema.dump(get_siswa)
        return make_response(jsonify({'message': 'update successful', 'result': result}), 209)
    # DELETE ONE SISWA
    if request.method == "DELETE":
        get_siswa = db.session.query(Siswa).get(nis)
        db.session.delete(get_siswa)
        db.session.commit()
        return make_response(jsonify({'message': 'delete successful'}), 204)
        
        
# @app.route('/siswa', methods=["POST"])
# def create_siswa():
    

if __name__ == "__main__":
    app.run(debug=True)