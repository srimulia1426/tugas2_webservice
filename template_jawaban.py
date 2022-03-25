# 6D/ 19090136/ Sri Mulia Ningsih
# 6D/ 19090060/ Nirla Wahidatus Salam

#username & password
#srimulia / 12345
#nirla / 12345


import os, random, string

from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tugas2.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    Token = db.Column(db.String(230), unique=True, nullable=True)

@app.route("/addUser", methods=["POST"])
def add_user():
    username = request.form['username']
    password = request.form['password']

    newUsers = User(username=username, password=password)

    db.session.add(newUsers)
    db.session.commit()
    return jsonify({
        'msg': 'berhasil menambahkan user',
        'username': username,
        'password' : password,
        'status' : 200
    })

@app.route("/api/v1/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
        User.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()

        return jsonify({
      'msg': 'Login berhasil',
      'username': username,
      'token': token,
      'status': 200 
      })

    else:
        return jsonify({
            'msg': 'Login gagal',
            'status' : 401,
        })

@app.route("/api/v2/users/info", methods=["POST"])
def info():
    token = request.values.get('token')
    user = user.query.filter_by(token=token).first()
    if user:
        return jsonify({
            'msg' : 'memasukan data berhasil',
            'username': user.username,
            'status': 200
        })
    else:
        return jsonify({
            'msg': 'salah menginputkan token'
         })

if __name__ == '__main__':
    app.run(debug = True, port=4000 )