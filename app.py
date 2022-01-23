from flask import Flask, request, jsonify
from flask import render_template
from firebase_admin import credentials, firestore, initialize_app

app = Flask ("BritCoin server")

# initialize firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

@app.route('/add', methods=['POST'])
def create():
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"an error occurred: {e}"

@app.route('/')
def hello ():
    return render_template('homepage.html')