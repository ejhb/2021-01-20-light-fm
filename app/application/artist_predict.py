import numpy as np # algèbre linéaire
import pandas as pd # procès de données, CSV file I/O (e.g. pd.read_csv)

import plotly 
import plotly.graph_objs as go
import matplotlib.pyplot as plt

import json
from flask import render_template

def data():
    plays = pd.read_csv('./data/user_artists.dat', sep='\t')
    artists = pd.read_csv('./data/artists.dat', sep='\t', usecols=['id','name'])

    # Merge artist and user pref data
    ap = pd.merge(artists, plays, how="inner", left_on="id", right_on="artistID")
    ap = ap.rename(columns={"weight": "playCount"})
    
    name_unique = list(set(ap['name']))
    return name_unique    