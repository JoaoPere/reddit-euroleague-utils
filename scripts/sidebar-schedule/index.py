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

def getScheduleTable(week):
	r = requests.get('https://www.euroleague.net/main/results?gamenumber={}&phasetypecode=RS&seasoncode=E2019'.format(week))
	
	soup = BeautifulSoup(r.text,'html.parser')
	
	reddit_table_head = appendTableDelimitors(TABLE_DELIM.join(['ROUND','DATE','HOME','AWAY','TIME']))
	reddit_cell_allignment = appendTableDelimitors(TABLE_DELIM.join([CELL_ALLIGNMENT] * 5))
	
	final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])
	
	# Result in 2nd element
	livescores = soup.find_all("div", class_="livescore")
	
	schedule_html = livescores[1]
	
	schedule_html_games = schedule_html.find_all("div", class_="game")
	
	cond_day = 0
	
	for idx, html_game in enumerate(schedule_html_games):
		both_clubs = html_game.find_all("div", class_="club")
		
		home_team_name = team_info_by_official.get(str(both_clubs[0].find("span", class_="name").get_text())).letter3_md
		away_team_name = team_info_by_official.get(str(both_clubs[1].find("span", class_="name").get_text())).letter3_md
		game_date = html_game.find("span", class_="date").get_text()
	
		# Removes "CET" from the string
		game_date = game_date.strip()[:len(game_date) - 4]
		game_date = datetime.strptime(game_date, "%B %d %H:%M")
	
		el_round = sys.argv[1] if idx == 0 else ""
		el_date = game_date.strftime("%b %d") if idx == 0 or (idx > 0 and int(game_date.day) != cond_day) else ""
	
		cond_day = game_date.day
	
		row_markdown = appendTableDelimitors(TABLE_DELIM.join([el_round, el_date, home_team_name, away_team_name, game_date.strftime("%H:%M")]))
	
		final_table = NEWLINE.join([final_table, row_markdown])
	
	return final_table

if __name__ == '__main__':
	print(getScheduleTable(sys.argv[1]))