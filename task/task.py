import json
from celery import Celery, group
from eternity import algo, config, puzzle, ind, tools
from web import config as web_config
app = Celery('task',  backend='rpc://', broker='pyamqp://guest@localhost//')

class Userspace():
  PIECES = ind.get_population()
  
  def __init__(self, user_id):
    self.user_id = user_id
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
@app.task
def get_userspace(user_id, erase=False):
  us = _get_userspace(user_id, erase=erase)
  return us.config

def _get_userspace(user_id, erase=False):
  global userspaces
  if user_id not in userspaces.keys() or erase:
    userspace = _create_userspace(user_id)
    userspaces[user_id] = userspace
  return userspaces[user_id]

def _create_userspace(user_id):
  usersp = Userspace(user_id)
  return usersp

@app.task(trail=True)
def run_puzzle(puzzle, ngen=0, **kwargs):
    return group(one_turn.s(puzzle, **kwargs) for i in range(ngen))()

@app.task(trail=True)
def one_turn(userspace, **kwargs):
#  algo.one_turn()
  return '{}'

@app.task
def get_config(user_id):
  userspace = _get_userspace(user_id)
  return userspace.config

@app.task
def set_config(user_id, **kwargs):
  userspace = _get_userspace(user_id)
  r = userspace.set_config(**kwargs)
  if r is not None:
    return r
  return userspace.config




