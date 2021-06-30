from flask.helpers import make_response
from flask.json import jsonify
from api import create_app

app = create_app()

# @app.route('/')
# def welcome():
#     return make_response(jsonify({'welcome': 'aboard'}), 200)

if __name__ == "__main__":
    app.run(debug=True)