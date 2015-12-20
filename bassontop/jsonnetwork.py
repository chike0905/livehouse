# coding: utf-8
import json
import time
import networkx as nx
import pylab
import matplotlib.pyplot as plt

from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

#jsonの読み込み
with open('2015artists.json', 'r') as f:
  artist_list = json.load(f)
with open('2015network.json', 'r') as f:
  artists = json.load(f)

#グラフオブジェクトの作成
G = nx.Graph()
#頂点の作成
for artist in artist_list:
  G.add_node(artist)

#エッジの作成
#artist_listよりartist毎に処理
for artist in artist_list:
  #artistsよりartistのデータを抽出
  for artistdata in artists:
    if artistdata["name"] is artist:
      #networkが存在するartist毎に処理
      for w_artists in artistdata["network"].keys():
        G.add_edge(artist,w_artists,weight= 10 / artistdata["network"][w_artists])

for artist in artist_list:
  if len(G.neighbors(artist)) is 0:
    G.remove_node(artist)

embed()
