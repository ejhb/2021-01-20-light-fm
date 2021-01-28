import numpy as np # algèbre linéaire
import pandas as pd # procès de données, CSV file I/O (e.g. pd.read_csv)

from plotly.offline import init_notebook_mode, iplot, plot
import plotly 
init_notebook_mode(connected=True)
import plotly.graph_objs as go

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import json
from flask import render_template

# Permet d'afficher les données disponibles dans le répertoire data
timesData = pd.read_csv("/Users/mosbahhachem/Documents/Cours/Data/timesData.csv")

def create_plot():
    # Prépare les trames de données (data frame)
    df = timesData.iloc[:100,:]


    # Création de la trame 1
    trace1 = go.Scatter(
                        x = df.world_rank,
                        y = df.citations,
                        mode = "lines",
                        name = "citations",
                        marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                        text = df.university_name)
    # Création de la trame 2
    trace2 = go.Scatter(
                        x = df.world_rank,
                        y = df.teaching,
                        mode = "lines+markers",
                        name = "enseignement",
                        marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                        text = df.university_name)

    data = [trace1, trace2]
    layout = dict(title = 'Citation et enseignement comparé au classement mondial des 100 meilleures universités',
                xaxis = dict(title = 'Rang Mondial',ticklen = 5,zeroline= False)
                )
    fig = dict(data = data, layout = layout)
    
    graphJSON = json.dumps (fig, cls = plotly.utils.PlotlyJSONEncoder) 
    
    return graphJSON
    