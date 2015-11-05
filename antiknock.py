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

print json.dumps(events,ensure_ascii=False,indent=4)
