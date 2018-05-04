import functools
from flask import Blueprint, flash, g, redirect, \
    render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username or not password:
      error = 'Username and Password are required.'
    elif db.execute('SELECT id FROM user WHERE username = ?', \
                    (username,)).fetchone() is not None:
      error = 'User {} is already registered.'.format(username)

    if error is None:
      c = db.execute(
          'INSERT INTO user (username, password) VALUES (?, ?)',
          (username, generate_password_hash(password))
      )
      db.commit()
      r = db.execute("SELECT * FROM user WHERE username = 'a'").fetchone()
      print r[0], r[1], r[2]
      return redirect(url_for('auth.login'))

    flash(error)

  return render_template('auth/register.html')

@blueprint.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None or not check_password_hash(user['password'], password):
      error = 'Incorrect username/password.'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('auth/login.html')

@blueprint.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


@blueprint.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)

  return wrapped_view
