# coding: utf-8
import urllib2
import json
from bs4 import BeautifulSoup
import HTMLParser
import time
import networkx as nx
import pylab
import matplotlib.pyplot as plt


def scraping(html):
  events = []
  soup = BeautifulSoup(html,"html.parser")
  artist_list = []
  event_lists = soup.find_all("div",class_="centerCont bottomLiner")
  for event_list in event_lists:
    title = event_list.find("p",class_="special_H2_pageLive_List")
    artists = event_list.find("strong")
    artist_lists = artists.text.split("/")
    artist_list = []
    for artist in artist_lists:
      artist_list.append(artist.strip())
    event = {}
    event["title"] = title.text
    event["artist"] = artist_list
    events.append(event)
  return events

start_t = time.clock()
events =[]
livehouses = [
    u"http://clubdrop.jp/",
    u"http://osaka-zeela.jp/",
    u"http://osaka-varon.jp/",
    u"http://seata.jp/",
    u"http://otsukadeepa.jp/",
    u"http://goith.jp/",
    u"http://vijon.jp/",
    u"http://deepa.jp/"
    ]
for livehouse in livehouses:
  for i in range(1,12):
    url = livehouse + u"live.html?y=2015&m=" + str(i)
    html = urllib2.urlopen(url)
    events = events + scraping(html)

scraping_t = time.clock()

'''
以下データ整形
arttist_list = ["バンド名"]
artist=[{
  "name":バンド名,
  "network":
    "バンド名":対バン回数
  }
]
'''
artists = []
artist_list = []
for event in events:
  for artist in event["artist"]:
    #artist名が長すぎるものを弾く
    if len(artist) < 50:
      #すでにartistsに情報があるか判定
      if artist not in artists:
        if artist not in artist_list:
          artist_list.append(artist)
        w_artists = []
        #artistが出てるイベントを抽出
        for eventdata in events:
          if artist in eventdata["artist"]:
            for eventartist in eventdata["artist"]:
              if eventartist is not artist:
                w_artists.append(eventartist)

        network = {}
        for w_artist in w_artists:
          if w_artist not in network:
            network[w_artist] = w_artists.count(w_artist)
        artistdata = {}
        artistdata["name"] = artist
        artistdata["network"] = network
        artists.append(artistdata)
format_time = time.clock()

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
        if artistdata["network"][w_artists] > 1:
          G.add_edge(artist,w_artists,weight= 10 / artistdata["network"][w_artists])

for artist in artist_list:
  if len(G.neighbors(artist)) < 1:
    G.remove_node(artist)

#レイアウトの最適化
pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=200, node_color="w")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos ,font_size=8, font_color="r")

network_time = time.clock()

degree = nx.degree(G)

# 表示
plt.show()

print "time for scraping  is " + str(scraping_t - start_t) + "sec"
print "time for data format is " + str(format_time - scraping_t) + "sec"
print "time for making graph is " + str(network_time - format_time) + "sec"
