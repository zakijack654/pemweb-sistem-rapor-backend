from flask import Blueprint, request, jsonify, make_response
from api.schema.periode_ajaran import PeriodeAjaranSchema
from api.models import PeriodeAjaran
from api import db

periode_ajaran = Blueprint('periode_ajaran', __name__)


@periode_ajaran.route('/periode_ajaran', methods=["GET", "POST"])
def get_post_periode():
    # GET ALL PERIODE AJARAN
    if request.method == "GET":
        all_periode = db.session.query(PeriodeAjaran).all()
        schema = PeriodeAjaranSchema(many=True)
        result = schema.dump(all_periode)
        return make_response(jsonify({"periode_ajaran": result}), 201)
    # POST PERIODE AJARAN
    elif request.method == "POST":
        params = request.form
        # Validate the form
        if not params.get('tahun_ajaran'):
            return make_response(jsonify({'error': 'Tahun Ajaran diperlukan!'}), 401)
        if not params.get('semester'):
            return make_response(jsonify({'error': 'Semester diperlukan!'}), 401)
        # Query to the model
        schema = PeriodeAjaranSchema()
        periode_ajaran = schema.load(params)
        db.session.add(periode_ajaran)
        db.session.commit()
        # make JSON response
        result = schema.dump(periode_ajaran)
        return make_response(jsonify({'message': 'post success', 'data': result}), 201)

@periode_ajaran.route('/periode_ajaran/<id>', methods=["GET", "DELETE", "PUT"])
def periode_by_id(id):
    # GET ONE PERIODE AJARAN
    if request.method == "GET":
        get_periode = db.session.query(PeriodeAjaran).get(id)
        schema = PeriodeAjaranSchema()
        result = schema.dump(get_periode)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)
    # UPDATE ONE PERIODE AJARAN
    elif request.method == "PUT":
        params = request.form
        # if periode_ajaran doesn't exist, reject request
        get_periode = db.session.query(PeriodeAjaran).get(id)
        if get_periode is None:
            return make_response(jsonify({'error': 'PeriodeAjaran not found!'}), 404)
        # Validate jenis_kelamin
        if params.get('semester') and params.get('semester') not in ('Ganjil', 'Genap'):
            return make_response(jsonify({'error': 'Semester tidak valid!'}), 400)
        # Update periode_ajaran based on params
        for p in params:
            setattr(get_periode, p, request.form[p])
        db.session.commit()
        # Create JSON response
        schema = PeriodeAjaranSchema()
        result = schema.dump(get_periode)
        return make_response(jsonify({'message': 'update successful', 'result': result}), 209)
    # DELETE ONE PERIODE AJARAN
    if request.method == "DELETE":
        get_periode = db.session.query(PeriodeAjaran).get(id)
        db.session.delete(get_periode)
        db.session.commit()
        return make_response(jsonify({'message': 'delete successful'}), 204)