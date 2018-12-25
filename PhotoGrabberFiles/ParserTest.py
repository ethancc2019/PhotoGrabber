from contextlib import closing
from html.parser import HTMLParser
import urllib.request as urllib2
from bs4 import BeautifulSoup
from requests import get, RequestException


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

if __name__ == "__main__":
    raw_html = simple_get("http://www.espn.com/college-football/player/_/id/4360056")
    prettyHtml = BeautifulSoup(raw_html,'html.parser')
    print(prettyHtml.select('h1')[0])

    splitName = str(prettyHtml.select('h1')[0]).replace("<h1>","").replace("</h1>","")
    print(splitName)
    #for p in  prettyHtml.select('h1'):
