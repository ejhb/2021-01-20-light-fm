# coding: utf8
from app import app 
from flask import request 
from app.models import *
from flask import render_template
from app.application.artist_predict import data , predict_artist_list


@app.route('/', methods =['GET','POST'])
def index():
  artist = data()
  artist_select = request.form.getlist("artist_select")
  artist_predict = predict_artist_list(artist_select)
  return render_template('index.html', artist = artist, artist_select = artist_select , artist_predict = artist_predict)