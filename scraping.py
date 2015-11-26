#  -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import HTMLParser

def antiknock(html):
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

def thegame(html):

  events = []
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
  return events
