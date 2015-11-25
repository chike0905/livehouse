# coding: utf-8
from bs4 import BeautifulSoup
import urllib2
import HTMLParser
import json

#スクレイピングするURLを指定
#HTML取得,soupオブジェクト生成
html = urllib2.urlopen(u"http://www.antiknock.net/schedule/")
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

#以下データ整形
artists = []
for event in events:
  for artist in event["artist"]:
    #すでにartistsに情報があるか判定
    if artist not in artists:
      w_artists = []
      #artistが出てるイベントを抽出
      #2015.11.25 TODO
      #自分が含まれるイベントが複数あった時、一つは自分を含んだままになってしまう
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
      """
          #出ているイベントの全出演者を追加
          for artistname in eventdata["artist"]:
            if artist not in artistname:
              w_artists.append(artistname)
      network = {}
      for artist in w_artists:
        if artist not in network:
          network[artist] = w_artists.count(artist)

      """

print json.dumps(artists,ensure_ascii=False,indent=4)
