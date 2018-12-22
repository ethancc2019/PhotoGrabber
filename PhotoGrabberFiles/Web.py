import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import webbrowser
import urllib.request

# Image URL
# http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/3125813.png

# Eventually change this to hold a list of all colleges
collegeUrl = "http://www.espn.com/college-football/team/roster/_/id/2132/cincinnati-bearcats"
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
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def downloader(image_url):
    global counter
    full_file_name = "test" + str(counter) + '.png'
    urllib.request.urlretrieve(image_url, full_file_name)
    counter += 1


if __name__ == "__main__":

    raw_html = simple_get(collegeUrl)
    strToMatch = "player/_/id/"
    bytes = str.encode("player/_/id/")
    location = -1;

    matches = re.findall("player/_/id/+[0-9]+", str(raw_html))

    idList = []
    string = matches[0]
    print(str(string).split("/id/"))
    test = str(string).split("/id/")
    print(test[1])

    for i in range(len(matches)):
        string = matches[i]
        # Splitting the found string
        test = str(string).split("/id/")
        # Appending the second element in the list which is the player ID
        idList.append(test[1])
        print(test[1])

    print("Removing Duplicates")
    #Thsi for-loop is used to get rid of the duplicates?
    finalId = []
    for i in idList:
        if i not in finalId:
            finalId.append(i)
            print(i)


    for i in range(10):

        urlTemp = "http://a.espncdn.com/combiner/i?img=/i/headshots/college-football/players/full/" + str(
            finalId[i]) + ".png"
        check = requests.get(urlTemp)
        if check.status_code != 404:
            webbrowser.open(urlTemp)