import os
import psycopg2
import random
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='templates', static_folder='shirts')

cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def create_accounts(conn):
  
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS accounts (username STRING, password STRING)"
        )
        cur.execute(
            "UPSERT INTO accounts (username, password) VALUES ('test', 'test2')")
        # logging.debug("create_accounts(): status message: %s",
        #               cur.statusmessage)
    conn.commit()

conn = psycopg2.connect(os.environ["DATABASE_URL"])

@app.route('/')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def pants():
  
  num = random.randint(10, 99)
  return render_template("pants.html", data=num)

@app.route('/signup', methods = ["GET"])
def signup():
  user = request.args.get('user')
  passw = request.args.get('pass')
  with conn.cursor() as cur:
    cur.execute("UPSERT INTO accounts (username, password) VALUES ('"+user+"', '"+passw+"')")
    conn.commit()
  
  return "submitted"

@app.route('/login', methods = ["GET"])

def login():
  user = request.args.get('user')
  passw = request.args.get('pass')
  with conn.cursor() as cur:
    cur.execute("SELECT * FROM accounts WHERE username='"+user+"' and password='"+passw+"'")
    res = cur.fetchall()
    print(len(res))
    str = ""
    if len(res) >= 1:
      str = "correct"
    else:
      str = "incorrect"
  return str

# @app.route('/pants')
# def pants():
#   num = random.randint(10, 99)
#   return render_template("pants.html", data=num)
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)

