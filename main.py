from flask import Flask
from app import api_bp
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()
app.register_blueprint(api_bp, url_prefix='/api')

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
  print("test2")
  if username in users:
    return users.get(username)
  return None

@app.route('/')
@auth.login_required

def hello_world():
  return "testNew"

if __name__ == '__main__':
  app.run()
