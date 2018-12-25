import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import webbrowser


"""
Global Variables
"""
collegeUrlList = []
espnLink = "http://www.espn.com"
ncaaTeams = "http://www.espn.com/college-football/teams"

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
    Main Driver
    """
if __name__ == "__main__":
    raw_html = simple_get(ncaaTeams)

    stringToFind = "/college-football/team/roster/"

    matches = re.findall(stringToFind + "_/id/[0-9]+/[a-z]+-[a-z]+-?[a-z]+", str(raw_html))

    for i in matches:
       print(i)