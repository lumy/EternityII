#!/usr/bin/env python

import os
from flask import Flask, session, redirect
from db import close_db, init_db
import auth
import dashboard

# create and configure the app
def create_app(test_config=None, env="production"):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
        SECRET_KEY='dev',
        ENV=env,
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  app.add_url_rule('/', 'index', hello)
  app.teardown_appcontext(close_db)
  app.register_blueprint(auth.blueprint)
  app.register_blueprint(dashboard.blueprint)

  return app

# a simple page that says hello
def hello():
  return redirect("dashboard.index") if "user_id" in session else  redirect("auth.login")

if __name__ == '__main__':
  from os import environ as env
  app = create_app(env="development")
  host = env.get("HOST", "localhost")
  port = env.get("PORT", 5000)
  debug = env.get("DEBUG", True)

  app.run(host=host, port=5000, debug=debug)
         
