from flask import session, g
import flask
from auth import login_required

blueprint = flask.Blueprint('dashboard', __name__, url_prefix='/dashboard')


@blueprint.route('/index', methods=('GET',))
@login_required
def index():
  return flask.render_template('index.html')

@blueprint.route('/test/<filename>', methods=('GET',))
def test(filename):
  return flask.render_template("%s.html" % filename)
