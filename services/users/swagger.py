import flask
from flask import current_app

from src.views import API

swagger_bp = flask.Blueprint('swagger', __name__, static_url_path='/swagger',
                             static_folder='swagger', template_folder='swagger')


@swagger_bp.route('/ui')
@swagger_bp.route('/ui/')
@swagger_bp.route('/ui/index.html')
def swagger_ui():
    scheme = flask.request.headers.get("X-Forwarded-Proto") or 'http'
    host = flask.request.host
    return flask.render_template('index.html', 
                                 url='{}://{}'.format(scheme, host))


@swagger_bp.route('/swagger-dynamic/swagger.json')
def swagger_dynamic():
    schema = API.__schema__
    schema.update({'schemes': ['http', 'https']})
    return flask.jsonify(schema)

