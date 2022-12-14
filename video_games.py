# -*- coding: utf-8 -*-
"""video_games.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-6n2YAiPtoxr8ez8Rp2MlUp7bb5kpzTM
"""

from google.colab import files
!pip install -q kaggle
files.upload()
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 /root/.kaggle/kaggle.json

import os

os.chdir("/content/drive/MyDrive/recomendation")

!kaggle datasets download -d deepcontractor/top-video-games-19952021-metacritic --unzip

import pandas as pd
data_games=pd.read_csv('/content/drive/MyDrive/recomendation/all_games.csv')

data_games.head(2)

df_cad = data_games
df_cad

df_cad.isna().any()

df_cad.dropna()

df_cad.drop(
    index = df_cad[df_cad['user_review']=="tbd"].index,
    inplace=True
)

from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer()
tf.fit(df_cad['name']) 
tf.get_feature_names()

tfidf_matrix = tf.fit_transform(df_cad['name']) 

tfidf_matrix.shape

tfidf_matrix.todense()

pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=df_cad.platform
).sample(22, axis=1).sample(10, axis=0)

from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

import numpy as np

def game_recomedations(game_name, items=df_cad[['name', 'platform']], k=5): 
  
    
    closest = df_cad.drop(game_name, errors='ignore')
    closest['index'] = [i for i in range(closest.shape[0])]

    index = closest[closest['name'] == game_name]['index'].values[0]

    sim_games = list(enumerate(cosine_sim[index]))
    sorted_sim_games = sorted(sim_games,key=lambda x:x[1],
                              reverse=True)[1:6]

    games = []
    for i in range(k):
      games.append(closest[closest['index'] == sorted_sim_games[i][0]]['name'].item())
    
    return pd.DataFrame({'name':games}).merge(items).head(k)

game_recomedations('Bloody Good Time')