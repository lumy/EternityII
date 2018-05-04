
import flask

blueprint = flask.Blueprint('dashboard', __name__, url_prefix='/dashboard')

@blueprint.route('/index', methods=('GET',))
def index():
  return 'Hello World!'

