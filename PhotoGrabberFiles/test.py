"""
Author: Ethan Collins
"""


import requests
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import webbrowser

# import pyodbc

# Image URL
# http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/3125813.png

# List to hold all of the college team URLs
collegeUrlList = []

# Dictonary to hold espn ids and player names
espnDictonary = {}

# Base link that will be used for parsing the main espn team page
ncaaTeams = "http://www.espn.com/college-football/teams"
espnPlayer = "http://www.espn.com/college-football/"
# String to append to to get valiv team link
espnLink = "http://www.espn.com"

# List to hold all of our appended team links
fullLink = []

# List to hold our

# Unambigious counter lol
counter = 0

# Instead of having to keep running this test if something crashes let's write to a file
fileHandle = open("file.txt", "w")


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


"""
Function returns all team roster links on ESPN
example: /college-football/team/roster/_/id/2132/cincinnati-bearcats
        /college-football/team/roster/_/id/151/east-carolina-pirates
        
append these results to "http://www.espn.com" to be taken to the roster page for that team
"""


def getTeamUrls():
    global ncaaTeams
    raw_team_html = simple_get(ncaaTeams)

    stringToFind = "/college-football/team/roster/"

    results = re.findall(stringToFind + "_/id/[0-9]+/[a-z]+-[a-z]+-?[a-z]+", str(raw_team_html))
    return results


"""
Funtion that connects to our server(warroom.stl.nfl.net) and connects to the database(RadarDB) and will return a list 
containing each player's first and last name with their MasterPlayerID
"""


# def getDatabaseResults():
#     connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                                 "Server=warroom.stl.nfl.net;"
#                                 "Database=RadarDB;"
#                                 "Trusted_Connection=yes;")
#     cursor = connection.cursor()
#     # Can change this to and sql query we want and return all sorts of different results
#     cursor.execute(
#         "SELECT MasterPlayerID, ISNULL(FootballName, FirstName)FirstName, Lastname from POBase() where DraftYear > 2017")
#
#     results = cursor.fetchall()
#
#     # CLOSE OUR CONNECTIONS
#     cursor.close()
#     connection.close()
#
#     return results

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


"""
MAIN DRIVER
"""
if __name__ == "__main__":

    collegeUrlList = getTeamUrls()

    for i in collegeUrlList:
        fullLink.append(espnLink + str(i))

    matchesTemp = []
    thisCounter = 0

    print("Saving player names and ID to our dictonary")

    # Upon initial test my loop didn't break so I'll add a flag
    breakCounter = 0
    for i in fullLink:
        raw_html = simple_get(i)
        # Removing duplicates here
        matchesTemp = re.findall("player/_/id/[0-9]+", str(raw_html))
        final_Matches = Remove(matchesTemp)

        for j in final_Matches:
            # Grab the player page html
            raw_html = simple_get("http://www.espn.com/college-football/" + str(j))
            prettyHtml = BeautifulSoup(raw_html, 'html.parser')
            # print(prettyHtml.select('h1')[0])

            splitName = str(prettyHtml.select('h1')[0]).replace("<h1>", "").replace("</h1>", "")

            string = final_Matches[thisCounter]
            tempID = str(string).split("/id/")
            # idList.append(test[1])
            # nameEdit = str(splitName[1]).strip("\\']").strip("'").strip()

            espnDictonary[splitName] = tempID[1]
            fileHandle.write(splitName + "," + str(tempID[1]) + "\n")
            # print("Player Name: " + splitName)
            string = ""
            splitName = ""
            prettyHtml = ""
            raw_html = ""

            tempID.clear()
            thisCounter += 1

        print("Finished this link: " + str(i))
        breakCounter += 1
        if breakCounter > 258:
            break
        thisCounter = 0

    # Close and save the file
    fileHandle.close()

    print("Number of players: " + str(len(espnDictonary)))
    print("DONE!")

    """
    1) Here we will take our data base dictionary with player names and IDs in JAARS 
    and find their entry in our espn dictionary
    
    2) Once we find their profile page we check if that profile page has a head shot.
    Open the photo in a new tab, if status code != 404 then we have a valid headshot
    
    3) If a valid headshot is verified then we download it to our headshot folder in JAARS and here we can specify 
    a file name where we append that player's ID from JAARS + .png and save it to our directory.
    
    Example file name: 3917315.png (Kyler Murray)
    """

    # for i in range(len(finalId)):

    #   urlTemp = "http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/" + str(
    #      finalId[i]) + ".png"
    # check = requests.get(urlTemp)
    # if check.status_code != 404:
    #   webbrowser.open(urlTemp)
