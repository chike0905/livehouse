# coding: utf-8
from bs4 import BeautifulSoup
import urllib2
import HTMLParser
import json
import networkx as nx
import pylab
import matplotlib.pyplot as plt

def eventjson(html):
  soup = BeautifulSoup(html,"html.parser")

  event_ttls = soup.find_all("div",class_="sche_box_right")
  events = []
  for event_ttl in event_ttls:
    event_title = event_ttl.find("div",class_="sche_event_ttl")
    if event_title.a is not None:
      title = event_ttl.a.get_text(strip=True)
      artists = event_ttl.find("div",class_="artist_text")
      if artists is not None:
        event = {}
        artist = artists.get_text(strip=True)
        artist_lists = artist.split("/")

        artist_list = []
        for artist_name in artist_lists:
          artist_list.append(artist_name.strip())

        event["title"] = title
        event["artist"] = artist_list
        events.append(event)
  return events

events = []

#antiknockの2月以前が取得できないため3~12月に設定
for i in range(3,12):
  #スクレイピングするURLを指定
  #HTML取得,soupオブジェクト生成
  url = u"http://www.antiknock.net/schedule/2015/" + str(i)
  html = urllib2.urlopen(url)
  events = events + eventjson(html)


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
          G.add_edge(artist,w_artists,weight=artistdata["network"][w_artists])


#レイアウトの最適化
pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=200, node_color="w")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos ,font_size=8, font_color="r")

# 表示
plt.show()

