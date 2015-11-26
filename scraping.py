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
