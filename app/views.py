# coding: utf8
from app import app
from app.models import *
from flask import render_template
from app.application.artist_predict import data

@app.route('/')
def index():
  artist_name = data()
  return render_template('index.html', artist_name = artist_name)

  
