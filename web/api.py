import flask, json
import auth
import config as web_config

try:
  from eternity import algo, config, puzzle, ind, tools
except ImportError:
  import sys, os
  sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))
  from eternity import algo, config, puzzle, ind, tools

blueprint = flask.Blueprint('api', __name__, url_prefix='/api/v1')

class Userspace():
  PIECES = ind.get_population()
  
  def __init__(self, user_id, username):
    self.user_id = user_id
    self.username = username
    self.old_pop = False
    self.puzzle = tools.load_population(old_pop=self.old_pop)

    self.limit = {
      'ngen': web_config.Limit.NGEN,
      'mutate_inpd': web_config.Limit.mutate_inpd,
      'selection_ind_value_step': web_config.Limit.selection_ind_value_step,
      'elitism_percentage_start': web_config.Limit.elitism_percentage_start,
      'elitism_percentage_up': web_config.Limit.elitism_percentage_up,
      'gen_modulo_elitism': web_config.Limit.gen_modulo_elitism,
      'select_light': web_config.Limit.select_light,
      'select_medium': web_config.Limit.select_medium
    }
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
    error = ""
    for k,v in kwargs.iteritems():
      if len(v) != 1:
        raise Exception("Too Maany or to few args, %s" % v)
  
      v = self.limit[k][2](v[0])
      if self.limit[k][0] <= v and v <= self.limit[k][1]:
        self.config[k] = v
      else:
        error = self.limit[k][3]
        break
    
    if error != "":
      return { 'msg': error, }
    return None


userspaces = {}
def get_userspace(user_id):
  global userspaces
  if user_id not in userspaces.keys():
    userspace = _create_userspace()
    userspaces[user_id] = userspace
  return userspaces[user_id]
    
def _create_userspace():
  usersp = Userspace(flask.g.user[0], flask.g.user[1])
  flask.session['userspace'] = flask.g.user[0]
  return usersp

@blueprint.route('/config', methods=("POST", "GET"))
@auth.login_required
def _config():
  userspace = get_userspace(flask.g.user[0])
  if flask.request.method == "GET":
    return json.dumps(userspace.config)
  r = userspace.set_config(**flask.request.form)
  if r is not None:
    flask.abort(flask.Response(json.dumps(r), status=400))
  return json.dumps(userspace.config)

@blueprint.route('/run', methods=("POST", ))
@auth.login_required
def run():
  userspace = get_userspace(flask.g.user[0])
  ret = algo.loop(userspace.puzzle, False, \
                  nloop=userspace.config['ngen']) # , **flask.g.userspace.config)
  return json.dumps({'solution_found': ret})
