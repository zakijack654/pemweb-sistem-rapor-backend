from flask import Blueprint, request, jsonify, make_response
from api.schema.siswa import SiswaGetSchema, SiswaSchema
from api.models import Siswa, Kelas
from api import db

siswa = Blueprint('siswa', __name__)

@siswa.route('/siswa', methods=["GET", "POST"])
def get_post_delete_siswa():
    # GET ALL SISWA
    if request.method == "GET":
        all_siswa = db.session.query(Siswa).join(Kelas).all()
        schema = SiswaGetSchema(many=True)
        result = schema.dump(all_siswa)
        return make_response(jsonify({"siswa": result}), 201)
    # POST SISWA
    elif request.method == "POST":
        params = request.form
        # Validate the form
        if not params.get('nis'):
            return make_response(jsonify({'error': 'NIS diperlukan!'}), 401)
        if not params.get('nama_siswa'):
            return make_response(jsonify({'error': 'Nama diperlukan!'}), 401)
        if not params.get('email'):
            return make_response(jsonify({'error': 'Email diperlukan!'}), 401)
        if not params.get('jenkel'):
            return make_response(jsonify({'error': 'Jenkel diperlukan!'}), 401)
        if not params.get('id_kelas'):
            return make_response(jsonify({'error': 'id_kelas diperlukan!'}), 401)
        if params.get('jenkel') not in ('L', 'P'):
            return make_response(jsonify({'error': 'jenis kelamin tidak valid!'}), 401)
        # If siswa already exist, reject request
        if db.session.query(Siswa).get(params['nis']):
            return make_response(jsonify({'error': 'Siswa with this NIS already exist!'}), 401)

        schema = SiswaSchema()
        siswa = schema.load(params)
        db.session.add(siswa)
        db.session.commit()
        result = schema.dump(siswa)
        return make_response(jsonify({'message': 'post success', 'data': result}))

@siswa.route('/siswa/<nis>', methods=["GET", "DELETE", "PUT"])
def siswa_by_nis(nis):
    # GET ONE SISWA
    if request.method == "GET":
        get_siswa = db.session.query(Siswa).get(nis)
        schema = SiswaGetSchema()
        result = schema.dump(get_siswa)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)
    # UPDATE ONE SISWA
    elif request.method == "PUT":
        params = request.form
        print(params)
        get_siswa = db.session.query(Siswa).get(nis)
        # if siswa doesn't exist, reject request
        if get_siswa is None:
            return make_response(jsonify({'error': 'Siswa not found!'}), 404)
        # Update siswa based on params
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