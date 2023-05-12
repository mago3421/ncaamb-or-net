"""
Project: NCAA Men's Basketball Prediction
Module: Web data extraction
Notes: Requires Python 3.6+
"""

import os
import traceback
from bs4 import BeautifulSoup
from rateLimitedRequester import rateLimitedRequester

# URL for fetching games on that day
DATE_URL="https://www.sports-reference.com/cbb/boxscores/index.cgi?month=MM&day=DD&year=YYYY"
PARENT_URL="https://www.sports-reference.com"

# Season starts and end per year
SEASONS = { \
    "2022-2023": \
        {"start": {"y": 2022, "m": 12, "d": 1}, \
         "end": {"y": 2023, "m": 4, "d": 3}}, \
    "2021-2022": \
        {"start": {"y": 2021, "m": 11, "d": 8}, \
         "end": {"y": 2022, "m": 4, "d": 4}}, \
} # Originally d=7

# Days per month dictionary (NOTE: Python 3.6+ will maintain order by default for advancing month)
MONTHS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 30} # 12=31

# Top-level directory for data (Change as needed)
DATADIR = os.path.join(os.path.expanduser('~'), "ncaamb-or-net", "gamedata")

# Change URL for every new day
def changeURLDate(url, m, d, y):
    url = url.replace("MM", "{:02d}".format(m))
    url = url.replace("DD", "{:02d}".format(d))
    url = url.replace("YYYY", "{:04d}".format(y))
    return url

def processTeamData(gameDir, pageTables, team_Name, teamId, index):
    try:
        # Team 1 player stat Processing
        teamStats = pageTables[index].find("tbody").find_all("tr")
        # Open team 1 stat file
        teamFile = open("{}/{}.csv".format(gameDir, team_Name),"w+")
        # Get team 1 player stats
        for playerTr in teamStats:
            playerStats = []
            # Check for Reserves column
            if "Reserves" in playerTr.find(attrs={"data-stat":"player"}).text: continue
            playerStats.append(playerTr.find(attrs={"data-stat":"player"}).text) # Name
            playerStats.append(playerTr.find(attrs={"data-stat":"mp"}).text) # Minutes played
            playerStats.append(playerTr.find(attrs={"data-stat":"fg"}).text) # Field goals
            playerStats.append(playerTr.find(attrs={"data-stat":"fga"}).text) # Field goals attempted
            playerStats.append(playerTr.find(attrs={"data-stat":"fg2"}).text) # 2pt field goals
            playerStats.append(playerTr.find(attrs={"data-stat":"fg2a"}).text) # 2pt field goals
            playerStats.append(playerTr.find(attrs={"data-stat":"fg3"}).text) # 3pt field goals
            playerStats.append(playerTr.find(attrs={"data-stat":"fg3a"}).text) # 3pt field goals attempted
            playerStats.append(playerTr.find(attrs={"data-stat":"ft"}).text) # Free throws
            playerStats.append(playerTr.find(attrs={"data-stat":"fta"}).text) # Free throws attempted
            playerStats.append(playerTr.find(attrs={"data-stat":"orb"}).text) # Offensive rebounds
            playerStats.append(playerTr.find(attrs={"data-stat":"drb"}).text) # Defensive rebounds
            playerStats.append(playerTr.find(attrs={"data-stat":"trb"}).text) # Total rebounds
            playerStats.append(playerTr.find(attrs={"data-stat":"ast"}).text) # Assists
            playerStats.append(playerTr.find(attrs={"data-stat":"stl"}).text) # Steals
            playerStats.append(playerTr.find(attrs={"data-stat":"tov"}).text) # Turnovers
            playerStats.append(playerTr.find(attrs={"data-stat":"pf"}).text) # Personal fouls
            playerStats.append(playerTr.find(attrs={"data-stat":"pts"}).text) # Points
            # Write stats to file
            teamFile.write(','.join(playerStats))
            teamFile.write('\n')
        teamFile.close()
    # If there is an exception while processing the team information, print to log
    except Exception:
        print("Error processing team: {}\n".format(team_Name))
        tlog = open("{}/traceback{}.txt".format(gameDir, teamId), "w+")
        tlog.write('teamName={}\n'.format(team_Name))
        traceback.print_exc(file=tlog)
        tlog.close()

def recordGame(page, y, m, d):
    data = BeautifulSoup(page, 'html.parser')  
    # Line Score
    ls_table = data.find_all(id="all_line-score")
    # Temporary string holder
    temp = str(ls_table)
    # Remove comment tags
    ls_table = BeautifulSoup(temp.replace("<!--","").replace("-->",""), 'html.parser')
    trs = ls_table.find_all("tr")
    # Team 1 data
    team1_Name = trs[2].find(attrs={"data-stat":"team"}).text
    # Check if Team 1 has a link to player data
    team1_Link = trs[2].find(attrs={"data-stat":"team"}).find("a")
    # Replace spaces in team name with underscores
    team1_Name = team1_Name.replace(" ","-")
    # Strip other special characters
    team1_Name = team1_Name.replace("&","").replace("'","").replace("(","").replace(")","").replace(".","")
    # Get team 1 Scores
    team1_1HS = trs[2].find(attrs={"data-stat":"1"}).text # 1st Half Score
    team1_2HS = trs[2].find(attrs={"data-stat":"2"}).text # 2nd Half Score
    team1_TS = trs[2].find(attrs={"data-stat":"T"}).text # Total Score
    # Team 2 data
    team2_Name = trs[3].find(attrs={"data-stat":"team"}).text
    team2_Link = trs[3].find(attrs={"data-stat":"team"}).find("a")
    # Replace spaces in team name with underscores
    team2_Name = team2_Name.replace(" ","-")
    # Strip other special characters
    team2_Name = team2_Name.replace("&","").replace("'","").replace("(","").replace(")","").replace(".","")
    # Get team 2 Scores      
    team2_1HS = trs[3].find(attrs={"data-stat":"1"}).text # 1st Half Score
    team2_2HS = trs[3].find(attrs={"data-stat":"2"}).text # 2nd Half Score
    team2_TS = trs[3].find(attrs={"data-stat":"T"}).text # Total Score
    # Make directory for game
    gameDir = "{0}/{1}-{2}-{3}_{4}_{5}".format(DATADIR, "{:04d}".format(y),"{:02d}".format(m),"{:02d}".format(d), team1_Name, team2_Name)
    # Use relative path
    try:
        os.mkdir(gameDir)
    # Some games appear twice
    except FileExistsError:
        return
    # Write to file
    outcome = open("{}/outcome.csv".format(gameDir),"w+")
    outcome.write(str(",".join([team1_Name,team1_1HS,team1_2HS,team1_TS])))
    outcome.write('\n')
    outcome.write(str(",".join([team2_Name,team2_1HS,team2_2HS,team2_TS])))
    outcome.close()
    # End line score processing
    # Get the rest of statistic tables
    pageTables = data.find(id="boxes").find_all("table")
    # Process team 1 if available
    if team1_Link is not None:
        processTeamData(gameDir, pageTables, team1_Name, 1, 0)
    # Process team 2 if available
    if team2_Link is not None:
        processTeamData(gameDir, pageTables, team2_Name, 2, (2 if team1_Link is not None else 0))

def extractSeason(start, end):
    # Use rate-limiting class to limit requests to page at 20 per minute
    rlr = rateLimitedRequester(rpm=20)
    # Initialize start date to beginning of season
    y = start["y"]
    m = start["m"]
    d = start["d"]
    seasonOver = False
    # Outer season loop
    while(not seasonOver):
        # Loop through month
        while(d <= MONTHS[m]):
            # Change date for that day
            dayURL = changeURLDate(DATE_URL, m, d, y)
            print("dayURL: "+dayURL)
            # Get summary page for that day
            dayPage = rlr.rlrequest(dayURL)
            daySoup = BeautifulSoup(dayPage, 'html.parser')
            # Get links to men's games on that page if there are any
            gameDivs = daySoup.find_all("div", {"class":"game_summary nohover gender-m"})
            # Iterate through game divs
            for gameDiv in gameDivs:
                # For each men's game, get the link to the game
                gameLink = gameDiv.find("td", {"class":"right gamelink"}).find('a')
                # Some games have no record
                if gameLink is not None:
                    # Append parent URL to link
                    gameURL = PARENT_URL + gameLink["href"]
                    # Now process the game
                    gamePage = rlr.rlrequest(gameURL)
                    if gamePage is not None:
                        recordGame(gamePage, y, m, d)
            # Check for end of season and exit loop if true
            if (y == end["y"]) and (m == end["m"]) and (d == end["d"]):
                seasonOver = True
                break
            # Otherwise, advance day
            else:
                d += 1
        # Move onto next month
        m += 1
        # Reset days
        d = 1
        # Advance year if necessary
        if m == 13:
            m = 1
            y += 1
    

if __name__=="__main__":
    # Use local variable to store copy of top-level
    originalDir = DATADIR
    # Now change DATADIR to season-specific
    DATADIR = os.path.join(originalDir,"2022-2023")
    try:
        os.mkdir(DATADIR)
    except FileExistsError:
        pass
    extractSeason(start=SEASONS["2022-2023"]["start"], end={"y":"2022","m":"3","d":"12"})
    # Now change DATADIR to season-specific
    DATADIR = os.path.join(originalDir,"2021-2022")
    try:
        os.mkdir(DATADIR)
    except FileExistsError:
        pass
    extractSeason(start=SEASONS["2021-2022"]["start"], end=SEASONS["2021-2022"]["end"])
