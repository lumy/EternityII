
import sqlite3
from flask import current_app, g

def get_db():
  if 'db' not in g:
    g.db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row

  return g.db


def close_db(e):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db(r):
    db = get_db()
    try:
      with current_app.open_resource('schema/sqlite/schema.sql') as f:
          db.executescript(f.read().decode('utf8'))
    except Exception as e:
      print e

