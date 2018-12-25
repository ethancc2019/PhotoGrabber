import urllib.request
import webbrowser

import requests

espnPlayers = {}
validPhotosUrl = []
fileHandle = open("file.txt", "w")

f = open("ValidPhotoUrls","w+")
with open("MASTERPLAYERS(ESPN).txt") as f:
    for line in f:
        splitValue = line.split(",")
        espnPlayers[splitValue[0]] = splitValue[1]

        # reset values
        splitValue = ""

    counter = 0
    for key, value in espnPlayers.items():

        iD = espnPlayers.get(key)
        strip = iD.split("\n")
        url = "http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/" + str(
            strip[0]) + ".png"
        check = requests.get(url)
        if check.status_code != 404:
            # webbrowser.open(urlTemp)
            #urllib.request.urlretrieve(url, '/Users/EthanCC/Desktop/HeadShots/' + str(strip[0]) + ".png")
            validPhotosUrl.append(url)
            fileHandle.write(url + " =>" + str(espnPlayers[key]) + "\n")
        counter += 1
        print("counter at: " + str(counter))
        if counter > 14500: break
print("Lenth of valid ID photos: " + str(len(validPhotosUrl)))