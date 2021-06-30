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