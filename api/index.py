from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'gauravv._.'


