import re
import urllib
import webbrowser

rosterUrl = 'http://www.espn.com/college-football/player/_/id/4038941'
id= rosterUrl.split("id/", 1)

print(id[1])

photoUrl = "http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/"

photoUrl += id[1]
photoUrl += ".png"
webbrowser.open(photoUrl)
