# coding: utf-8
import urllib2
import json
from bs4 import BeautifulSoup
import HTMLParser

events = []

url = u"http://www.shibuyathegame.com/2015_6.html"
html = urllib2.urlopen(url)
soup = BeautifulSoup(html,"html.parser")
title = None
artist_list = []
event_colums = soup.find_all("div",class_="set-l")
for event_colum in event_colums:
  event_ttls = event_colum.find_all("span",class_="fsize_ll")
  event_texts = event_colum.find("p")
  event = {}
  for event_ttl in event_ttls:
    big_text = event_ttl.string
    if big_text.isdigit() is False:
      #曜日がbig_textに含まれるか判定
      weeks = ["SUN","MON","TUE","WED","THU","FRI","SAT"]
      flag = False
      for day in weeks:
        if day in big_text:
          flag = True
          break
      if flag is False:
        title = big_text
  artist_list = []
  for text in event_texts.strings:
    raw_text = text.strip()
    if raw_text:
      if "<" not in raw_text and "ADV" not in raw_text and "OPEN" not in raw_text:
        artist_list.append(raw_text)
  event["title"] = title
  event["artist"] = artist_list
  events.append(event)
print json.dumps(events,sort_keys=True, indent=4)
