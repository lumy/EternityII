
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello'

if __name__ == '__main__':
  from os import environ as env
  host = env.get("HOST", "localhost")
  port = env.get("PORT", 5000)
  debug = env.get("DEBUG", True)
  app.run(host=host, port=5000, debug=debug)
         
