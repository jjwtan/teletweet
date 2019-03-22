from bs4 import BeautifulSoup, SoupStrainer
import requests
import sys

def get_stats(url):
    if "twitter" not in url:    # if not twitter link
        return ("1000","1000")
    try:
        r = requests.get(url)
    except:
        return ("1000","1000")
    strainer = SoupStrainer('div', attrs={'class': 'js-tweet-stats-container tweet-stats-container'})
    soup = BeautifulSoup(r.content, 'html.parser', parse_only=strainer)

    retweets = likes = "0"

    try:
        retweets = soup.find(class_="request-retweeted-popup")['data-compact-localized-count']
    except:
        pass
    try:
        likes = soup.find(class_="request-favorited-popup")['data-compact-localized-count']
    except:
        pass

    return (retweets, likes)


# result = get_stats(sys.argv[1])
# print("retweets: %s \nlikes: %s" % result)