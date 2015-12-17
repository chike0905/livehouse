# coding: utf-8
import urllib2
import json
from bs4 import BeautifulSoup
import HTMLParser

events = []

url = u"http://otsukadeepa.jp/live.html?y=2015&m=12"
html = urllib2.urlopen(url)
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

print json.dumps(events,sort_keys=True, indent=4)
