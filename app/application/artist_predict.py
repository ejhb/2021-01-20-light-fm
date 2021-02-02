import numpy as np # algèbre linéaire
import pandas as pd # procès de données, CSV file I/O (e.g. pd.read_csv)

from lightfm import LightFM
from lightfm.evaluation import auc_score, precision_at_k, recall_at_k
from lightfm.cross_validation import random_train_test_split
from lightfm.data import Dataset
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix

import plotly 
import plotly.graph_objs as go
import matplotlib.pyplot as plt

import json
from flask import render_template


plays = pd.read_csv('app/data/user_artists.dat', sep='\t')
artists = pd.read_csv('app/data/artists.dat', sep='\t', usecols=['id','name'])
ap = pd.merge(artists, plays, how="inner", left_on="id", right_on="artistID")
ap = ap.rename(columns={"weight": "playCount"})
 # Group artist by name
artist_rank = ap.groupby(['name']) \
    .agg({'userID' : 'count', 'playCount' : 'sum'}) \
    .rename(columns={"userID" : 'totalUsers', "playCount" : "totalPlays"}) \
    .sort_values(['totalPlays'], ascending=False)

artist_rank['avgPlays'] = artist_rank['totalPlays'] / artist_rank['totalUsers']

# Merge into ap matrix
ap = ap.join(artist_rank, on="name", how="inner") \
    .sort_values(['playCount'], ascending=False)

# Preprocessing
pc = ap.playCount
play_count_scaled = (pc - pc.min()) / (pc.max() - pc.min())
ap = ap.assign(playCountScaled=play_count_scaled)
#print(ap)

def data():
    # Merge artist and user pref data
    name_unique = list(set(ap['name']))
    return name_unique  

def predict_artist_list(artist_select): 
# Build a user-artist rating matrix 
    ratings_df = ap.pivot(index='userID', columns='artistID', values='playCountScaled')
    ratings = ratings_df.fillna(0).values

    artist_names = ap.sort_values("artistID")["name"].unique()

    add_user = [0]*17632

    new_list = []

    for item in artist_select:
        artists_idx = artists.index[artists["name"] == item]
        new_list.append(artists_idx)
        for i in new_list : 
            for j in i :
                index = j 
                add_user[index] = 1
            new_ratings_df = np.vstack((ratings_df, add_user))
            ratings_df = pd.DataFrame(new_ratings_df)
    new_userID = (ratings_df.shape[0] - 1)     
    ratings = ratings_df.fillna(0).values

    # Build a sparse matrix
    X = csr_matrix(ratings)

    n_users, n_items = ratings_df.shape

    user_ids = ratings_df.index.values
    artist_names = ap.sort_values("artistID")["name"].unique()


    # Build data references + train test
    Xcoo = X.tocoo()
    data = Dataset()
    data.fit(np.arange(n_users), np.arange(n_items))
    interactions, weights = data.build_interactions(zip(Xcoo.row, Xcoo.col, Xcoo.data)) 
    train, test = random_train_test_split(interactions)



    model = LightFM(learning_rate=0.05, loss='warp')
    model.fit(train, epochs=10, num_threads=2)


    # Predict
    scores = model.predict(0, np.arange(n_items))
    top_items = artist_names[np.argsort(-scores)]
    return top_items[0:10]


