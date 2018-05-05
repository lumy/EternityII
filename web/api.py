import flask, json
import auth

try:
  from eternity import algo, config
except ImportError:
  import sys, os
  sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))
  from eternity import algo, config

blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')

class Userspace():

  def __init__(self, user_id, username):
    self.user_id = user_id
    self.username = username
    self.config = {
      'ngen': config.NGEN,
      'mutate_inpd': config.mutate_inpd,
      'selection_ind_value_step': config.selection_ind_value_step,
      'elitism_percentage_start': config.elitism_percentage_start,
      'elitism_percentage_up': config.elitism_percentage_up,
      'gen_modulo_elitism': config.gen_modulo_elitism,
      'select_light': config.select_light,
      'select_medium': config.select_medium
    }

  def set_config(self, **kwargs):
    pass

def _create_userspace():

  if not 'userspace' in flask.g:
    flask.g.userspace = Userspace(flask.g.user[0], flask.g.user[1])


@blueprint.route('/config', methods=("POST", "GET"))
@auth.login_required
def _config():
  _create_userspace()
  if flask.request.method == "GET":
    return json.dumps(flask.g.userspace.config)
  flask.g.userspace.set_config(**flask.request.form)
  return json.dumps(flask.g.userspace.config)

@blueprint.route('/run', methods=("Post", ))
@auth.login_required
def run():
  _create_userspace()
