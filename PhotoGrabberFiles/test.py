import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import webbrowser
import pyodbc

# Image URL
# http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/3125813.png

# List to hold all of the college team URLs
collegeUrlList = []

#Dictonary to hold espn ids and player names
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


def getDatabaseResults():
    connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                "Server=warroom.stl.nfl.net;"
                                "Database=RadarDB;"
                                "Trusted_Connection=yes;")
    cursor = connection.cursor()
    # Can change this to and sql query we want and return all sorts of different results
    cursor.execute(
        "SELECT MasterPlayerID, ISNULL(FootballName, FirstName)FirstName, Lastname from POBase() where DraftYear > 2017")

    results = cursor.fetchall()

    # CLOSE OUR CONNECTIONS
    cursor.close()
    connection.close()

    return results


"""
MAIN DRIVER
"""
if __name__ == "__main__":

    collegeUrlList = getTeamUrls()

    for i in collegeUrlList:
        fullLink.append(espnLink + str(i))

    matchesTemp = []
    thisCounter = 0

    # This lost will contains duplicates so we will have to deal with that
    idList = []
    for i in fullLink:
        raw_html = simple_get(i)
        matchesTemp = re.findall("player/_/id/[0-9]+", str(raw_html))
        for j in matchesTemp:
            #Grab the player page html
            playerPage = simple_get(espnPlayer + str(j))
            urlTest = requests.request(playerPage)
            #Grab the name
            name = re.findall("<h1>[A-Z]{1}[a-z]+\s[A-Z]{1}[']?[A-Z]?[-]?[A-Z]?[a-z]+", str(playerPage))
            #split the name from it's <h1> tag
            splitName = str(name).split("<h1>")

            string = matchesTemp[thisCounter]
            test = str(string).split("/id/")
            #idList.append(test[1])
            nameEdit = str(splitName[1]).strip("\\']").strip("'").strip()


            espnDictonary[nameEdit] = test[1]
            string = ""
            test.clear()
            thisCounter += 1
            splitName = ""
        thisCounter = 0

    for key, val in espnDictonary.items():
        print (key, "=>", val)

    # Thsi for-loop is used to get rid of the duplicates?
    finalId = []
    for i in idList:
        if i not in finalId:
            finalId.append(i)
            print(i)

    # for i in range(len(finalId)):

    #   urlTemp = "http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/" + str(
    #      finalId[i]) + ".png"
    # check = requests.get(urlTemp)
    # if check.status_code != 404:
    #   webbrowser.open(urlTemp)
