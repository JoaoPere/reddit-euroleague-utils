import requests
from bs4 import BeautifulSoup
import praw
import sys
from datetime import datetime, timezone, tzinfo

sys.path.append('..')

from team_structs import team_info_by_official

CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'

def appendTableDelimitors(content):
	return TABLE_DELIM + content + TABLE_DELIM

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
	
	for idx, html_game in enumerate(schedule_html_games):
		both_clubs = html_game.find_all("div", class_="club")
		
		home_team_name = team_info_by_official.get(str(both_clubs[0].find("span", class_="name").get_text())).letter3_md
		home_team_score = both_clubs[0].find("span", class_="score").attrs['data-score']
	
		away_team_name = team_info_by_official.get(str(both_clubs[1].find("span", class_="name").get_text())).letter3_md
		away_team_score = both_clubs[1].find("span", class_="score").attrs['data-score']
	
		el_round = sys.argv[1] if idx == 0 else ""
		result = "[{}-{}]()".format(home_team_score, away_team_score)
	
		row_markdown = appendTableDelimitors(TABLE_DELIM.join([el_round, home_team_name, away_team_name, result]))
	
		final_table = NEWLINE.join([final_table, row_markdown])
	
	return final_table

if __name__ == '__main__':
	print(getResultsTable(sys.argv[1]))