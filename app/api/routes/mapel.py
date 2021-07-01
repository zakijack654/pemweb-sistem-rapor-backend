from flask import Blueprint, request, jsonify, make_response
from api.schema.mapel import MapelSchema
from api.models import Mapel, Jurusan
from api import db

mapel = Blueprint('mapel', __name__)

@mapel.route('/mapel', methods=['GET', 'POST'])
def get_post_jurusan():
    # GET ALL JURUSAN
    if request.method == "GET":
        all_jurusan = db.session.query(Mapel).join(Jurusan).all()
        schema = MapelSchema(many=True)
        result = schema.dump(all_jurusan)
        return make_response(jsonify({"jurusan": result}), 201)
    # POST JURUSAN
    elif request.method == "POST":
        params = request.form
        # Validate the form
        if not params.get('nama_mapel'):
            return make_response(jsonify({'error': 'Nama mapel diperlukan!'}), 400)
        if not params.get('id_jurusan'):
            return make_response(jsonify({'error': 'ID Jurusan diperlukan!'}), 400)
        # Query to the model
        schema = MapelSchema()
        mapel = schema.load(params)
        db.session.add(mapel)
        db.session.commit()
        # make JSON response
        result = schema.dump(mapel)
        return make_response(jsonify({'message': 'post success', 'data': result}), 201)