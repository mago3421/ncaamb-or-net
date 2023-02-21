"""
Project: NCAA Men's Basketball Prediction
Module: Web data extraction
Notes: Requires Python 3.6+
"""

from bs4 import BeautifulSoup
import subprocess
import csv
import os
from rateLimitedRequester import rateLimitedRequester

# URL for fetching games on that day
DATE_URL="https://www.sports-reference.com/cbb/boxscores/index.cgi?month=MM&day=DD&year=YYYY"
PARENT_URL="https://www.sports-reference.com"

# Season starts and end per year
SEASONS = { \
    "2022-2023": \
        {"start": {"y": "2022", "m": "11", "d": "7"}, \
         "end": {"y": "2023", "m": "4", "d": "3"}}, \
}

# Days per month dictionary (NOTE: Python 3.6+ will maintain order by default for advancing month)
MONTHS = {'1': 31, '2': 29, '3': 31, '4': 30, '5': 31, '6': 30, '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}

# Top-level directory for data (Change as needed)
DATADIR = os.path.join(os.path.expanduser('~'), "ncaamb-or-net", "gamedata")

# Returns true if date1 is past date2, else false
def isDatePast(date1, date2):
    return (date1 > date2)

# Change URL for every new day
def changeURLDate(url, m, d, y):
    url = url.replace("MM", m)
    url = url.replace("DD", d)
    url = url.replace("YYYY", y)
    return url

def recordGame(page, year, month, day):
    #TODO: Add logic to parse game and record line score in one file
    # and player stats into two separate CSV files for each team
    #gameSoup = BeautifulSoup(page.text, 'html.parser')
    #lineScore = gameSoup.find("table", {"id":"line-score"}) # Not working
    # glstable = gsoup.find_all("table", {"id":"line-score"})
    pass

def extractSeason(start, end):
    #TODO: Add logic to iterate through season dates
    y = start.y
    m = start.m
    d = start.d
    # Use rate-limiting class to limit requests to page at 20 per minute
    rlr = RateLimitedRequester(rpm=20)
    dayURL = changeURLDate(DATE_URL, "01","01","2022")
    # Get summary page for that day
    dayPage = rlr.rlrequest(url=dayURL)
    daySoup = BeautifulSoup(dayPage.text, 'html.parser')
    # Get links to men's games on that page if there are any
    gameDivs = find_all("div", {"class":"game_summary nohover gender-m"})
    # Iterate through game divs
    for gameDiv in gameDivs:
        # For each men's game, get the link to the game
        gameLinkTd = gameDiv.find("td", {"class","right gamelink"})
        # Append parent URL to link
        gameURL = PARENT_URL + gameLinkTd.find('a')["href"] 
        # Now process the game
        gamePage = rlr.rlrequest(url=gameURL)
        recordGame(gamePage, y, m, d)
    

if __name__=="__main__":
    extractSeason(start=SEASONS["2022-2023"].start, end={"y":"2022","m":"2","d":"20"})
