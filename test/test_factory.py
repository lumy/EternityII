
from web.route import create_app
from web.db import get_db, init_db
from flask import g, session
import pytest, sqlite3

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_get_close_db(app):
  with app.app_context():
    db = get_db()
    assert db is get_db()

  with pytest.raises(sqlite3.ProgrammingError) as e:
    db.execute('SELECT 1')

  assert 'closed' in str(e)


def test_register(client, app):
  assert client.get('/auth/register').status_code == 200
  response = client.post(
      '/auth/register', data={'username': 'a', 'password': 'a'}
  )
  assert 'http://localhost/auth/login' == response.headers['Location']

  with app.app_context():
    assert get_db().execute(
        "select * from user where username = 'a'",
    ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username and Password are required.'),
    ('a', '', b'Username and Password are required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
  response = client.post(
      '/auth/register',
      data={'username': username, 'password': password}
  )
  assert message in response.data

def test_login(client, auth):
  assert client.get('/auth/login').status_code == 200
  response = auth.login()
  assert response.headers['Location'] == 'http://localhost/dashboard/index'

  with client:
    client.get('/')
    assert session['user_logged'] == 1
    assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
  ('a', 'test', b'Incorrect username/password.'),
  ('test', 'a', b'Incorrect username/password.'),
))
def test_login_validate_input(auth, username, password, message):
  response = auth.login(username, password)
  assert message in response.data

def test_logout(client, auth):
  auth.login()
  with client:
    auth.logout()
    assert 'user_id' not in session
