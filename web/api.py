import flask, json
import auth
import config as web_config
from task import task

blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')

@blueprint.route('/init', methods=(["POST",]))
@auth.login_required
def init_userspace():
  config = task.get_userspace.delay(flask.g.user[0], flask.request.form.get('erase', False)).get(timeout=2)
  return json.dumps(config)
  
@blueprint.route('/config', methods=("POST", "GET"))
@auth.login_required
def _config():
  """
    We Don't delay the answer as should be very fast
  """
  if flask.request.method == "GET":
    config = task.get_config.delay(flask.g.user[0]).get(timeout=2)
    return json.dumps(config)

  r = task.set_config.delay(flask.g.user[0], **dict(flask.request.form)).get(timeout=2)
  return json.dumps(r)

@blueprint.route('/run', methods=("POST", ))
@auth.login_required
def run():
  """
    Hard limit on timer: 120minutes (which should be waaaaayyyyy enough)
    using write_stats to False to not break old usage. but everything should be in db.
  """
  r = task.run_puzzle(flask.g.user[0])
  return '' # json.dumps({})
