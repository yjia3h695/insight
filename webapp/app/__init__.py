from flask import Flask
app = Flask(__name__)
app.secret_key = 'Guess Who?'
from app import views

