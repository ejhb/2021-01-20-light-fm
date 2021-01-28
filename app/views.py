# coding: utf8
from app import app
from app.models import *
from flask import render_template
from app.application.artist_predict import *

@app.route('/')
def index():
  artist_name = data()
  return render_template('index.html', plot= artist_name)

  
