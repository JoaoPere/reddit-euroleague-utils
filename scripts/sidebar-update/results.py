import requests
from bs4 import BeautifulSoup
import sys
from collections import namedtuple
from datetime import datetime, timezone, tzinfo
import praw
import os

sys.path.append('..')

from team_structs import team_info_by_official
from prepare_dot_env import prepareDotEnv

CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'

def appendTableDelimitors(content):
	return TABLE_DELIM + content + TABLE_DELIM
   
# Returns the href to the result thread 
# For now, only covering regular season  
def getResultThread(home_team, away_team, el_round, new_submissions):
	reddit_home_team = team_info_by_official.get(home_team).reddit
	reddit_away_team = team_info_by_official.get(away_team).reddit
	
	#TODO: Change title to constant?
	for submission in new_submissions:
		if submission.title == 'Post-Match Thread: {home_team} - {away_team} [EuroLeague Regular Season, Round {el_round}]'.format(home_team=reddit_home_team, away_team=reddit_away_team, el_round=el_round):
			return submission.url
		
	return None

# TODO: Add support to playoffs
def getResultsTable(week):
	r = requests.get('https://www.euroleague.net/main/results?gamenumber={}&phasetypecode=RS&seasoncode=E2019'.format(week))
	
	soup = BeautifulSoup(r.text,'html.parser')
	
	reddit_table_head = appendTableDelimitors(TABLE_DELIM.join(['ROUND','HOME','AWAY','RESULT']))
	reddit_cell_allignment = appendTableDelimitors(TABLE_DELIM.join([CELL_ALLIGNMENT] * 4))
	
	final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])
	
	# Result in 2nd element
	livescores = soup.find_all("div", class_="livescore")
	
	schedule_html = livescores[1]
	
	schedule_html_games = schedule_html.find_all("div", class_="game")

	reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
						client_secret=os.getenv("REDDIT_APP_SECRET"),
						password=os.getenv("REDDIT_PASSWORD"),
						username=os.getenv("REDDIT_ACCOUNT"),
						user_agent="r/EuroLeague Post Game Thread Generator Script")
	
	el_sub = reddit.subreddit('Euroleague')

	# Since new returns an iterator, it's obligatory to convert to list so that elements are not consumed
	new_submissions = list(el_sub.new(limit=100))
	
	for idx, html_game in enumerate(schedule_html_games):
		both_clubs = html_game.find_all("div", class_="club")
		
		home_team_official = both_clubs[0].find("span", class_="name").text
		away_team_official = both_clubs[1].find("span", class_="name").text
		
		home_team_name = team_info_by_official.get(home_team_official).letter3_md
		home_team_score = both_clubs[0].find("span", class_="score").attrs['data-score']
	
		away_team_name = team_info_by_official.get(away_team_official).letter3_md
		away_team_score = both_clubs[1].find("span", class_="score").attrs['data-score']
	
		# Only assign to the first row of the table - Reddit markdown syntax related
		el_round = str(week) if idx == 0 else ""
		
		submission_url = getResultThread(home_team_official, away_team_official, str(week), new_submissions)
		
		result = "[{home_team_score}-{away_team_score}]({submission_url})".format(home_team_score=home_team_score, away_team_score=away_team_score,submission_url=submission_url)
	
		row_markdown = appendTableDelimitors(TABLE_DELIM.join([el_round, home_team_name, away_team_name, result]))
	
		final_table = NEWLINE.join([final_table, row_markdown])
		
	final_table = NEWLINE.join([final_table, '**Note:** Access the post-match threads by clicking in the result'])
	
	return final_table

if __name__ == '__main__':
	print(getResultsTable(sys.argv[1]))