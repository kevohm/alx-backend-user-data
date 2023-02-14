#!/usr/bin/env python3
"""app module
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if(AUTH.valid_login(email, password)):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res
    return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
