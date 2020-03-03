import requests
from bs4 import BeautifulSoup
import praw
from pprint import pprint
from collections import namedtuple
from datetime import datetime, timedelta
import re
import sys
from requests.adapters import HTTPAdapter
import os

sys.path.append('..')

from team_structs import team_info_by_fs
from prepareDotEnv import prepareDotEnv

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=sys.maxsize))
s.mount('https://', HTTPAdapter(max_retries=sys.maxsize))

TABLE_DELIM = '|'
NEWLINE = '\n'

NUMBER = '#'
PLAYER = 'PLAYER'
MINUTES = 'MIN'
POINTS = 'PTS'
FG2 = '2FG'
FG3 = '3FG'
FREE_TRHOWS = 'FT'
OFF_REBOUNDS = 'OREB'
DEF_REBOUNDS = 'DREB'
TOT_REBOUNDS = 'TREB'
ASSISTS = 'AST'
STEALS = 'STL'
TURNOVERS = 'TO'
BLOCKS = 'BLK'
#BLOCKS_AGAINST = 'Ag'
FOULS_COMMITED = 'PF'
#FOULS_RECEIVED = 'Rv'
PIR = 'PIR'
REDDIT_HR = NEWLINE + '----' + NEWLINE

REDDIT_THREAD_PLACEHOLDER_TEXT = 'Thread will be updated soon with more information'

CELL_ALLIGNMENT = ':-'

prepareDotEnv()

reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
					client_secret=os.getenv("REDDIT_APP_SECRET"),
					password=os.getenv("REDDIT_PASSWORD"),
					username=os.getenv("REDDIT_ACCOUNT"),
					user_agent="r/EuroLeague Post Game Thread Generator Script")

el_sub = reddit.subreddit('Euroleague')

def appendTableDelimitors(content):
	return TABLE_DELIM + content + TABLE_DELIM

def getRedditTableHeadAndCellAlignment(table_head):
	# Formatting table headings
	reddit_table_head = appendTableDelimitors(TABLE_DELIM.join(table_head))

	# Reddit cell alignment
	reddit_cell_allignment = appendTableDelimitors(TABLE_DELIM.join([CELL_ALLIGNMENT] * len(table_head)))

	return NEWLINE.join([reddit_table_head, reddit_cell_allignment])

def bold(text):
	return '**' + text + '** '

def getQuarterScoresMarkdown(soup, home_team, away_team):
	quarter_table = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_PartialsStatsByQuarter_dgPartials")
	quarter_table_rows = quarter_table.find_all('tr')

	final_table = getRedditTableHeadAndCellAlignment(['BY QUARTER','1','2','3','4'])

	for idx, row in enumerate(quarter_table_rows[1:]):
		quarter_table_cols = row.find_all('td')
		quarter_table_cols = [ele.text.strip() for ele in quarter_table_cols]

		# Overrides the team name
		quarter_table_cols[0] = team_info_by_fs.get(home_team).full_md if idx == 0 else team_info_by_fs.get(away_team).full_md

		cols_markdown = appendTableDelimitors(TABLE_DELIM.join(quarter_table_cols))

		final_table = NEWLINE.join([final_table, cols_markdown])

	return final_table

def getTablesMarkdown(soup, home_team_name, away_team_name):
	home_away_tables = soup.find_all(id='tblPlayerPhaseStatistics')
	
	home_table = home_away_tables[0]
	away_table = home_away_tables[1]

	home_coach = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_LocalClubStats_lblHeadCoach").text
	away_coach = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_RoadClubStats_lblHeadCoach").text

	return getTableMarkdown(home_table, home_team_name, home_coach), getTableMarkdown(away_table, away_team_name, away_coach)

def getTableMarkdown(table, name, coach):
	table_rows = table.find_all('tr')

	TEAM_MD = team_info_by_fs.get(name).full_md.upper()

	final_table = getRedditTableHeadAndCellAlignment([NUMBER, TEAM_MD, MINUTES, POINTS, FG2, FG3, FREE_TRHOWS, OFF_REBOUNDS, DEF_REBOUNDS, TOT_REBOUNDS, ASSISTS, STEALS, TURNOVERS, BLOCKS, FOULS_COMMITED, PIR])

	for idx, row in enumerate(table_rows[2: len(table_rows) - 1]):
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]

		# Removes the blocks against and fouls drawn columns
		cols.pop(16)
		cols.pop(14)

		cols_markdown = appendTableDelimitors(TABLE_DELIM.join(cols))
		final_table = NEWLINE.join([final_table, cols_markdown])

	head_coach_markdown = bold("Head Coach:") + coach
	final_table = NEWLINE.join([head_coach_markdown, NEWLINE, final_table])

	return final_table

def getFinalScoreMarkdown(home_team_name, home_team_score, away_team_name, away_team_score):
	final_table = getRedditTableHeadAndCellAlignment(['TEAM', 'SCORE'])

	home_team_md = team_info_by_fs.get(home_team_name).full_md
	away_team_md = team_info_by_fs.get(away_team_name).full_md

	home_team_name_score = appendTableDelimitors(TABLE_DELIM.join([home_team_md, home_team_score]))
	away_team_name_score = appendTableDelimitors(TABLE_DELIM.join([away_team_md, away_team_score]))

	final_table = NEWLINE.join([final_table, home_team_name_score, away_team_name_score])

	return final_table

def getGameInformationMarkdown(soup):
	date_stadium_info_div = soup.find('div', class_='dates')

	date_info_cet = (date_stadium_info_div.find('div', class_='date cet').text).replace('CET: ','') + ' CET'
	stadium_info = date_stadium_info_div.find('span', class_='stadium').text
	attendance_info = soup.find(id='ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_lblAudience').text
	referees_info = soup.find(id='ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_lblReferees').text

	date_info_cet_markdown = bold('Event Date:') + date_info_cet
	stadium_info_markdown = bold('Stadium:') + stadium_info
	attendance_info_markdown = bold('Attendance:') + attendance_info
	referees_info_markdown = bold('Referees:') + referees_info

	return NEWLINE.join([date_info_cet_markdown, NEWLINE, stadium_info_markdown, NEWLINE, attendance_info_markdown, NEWLINE, referees_info_markdown])

def getScoresTable(soup, home_team, away_team):
	home_team_score = soup.find(class_="sg-score").find(class_="local").find(class_="score").text
	away_team_score = soup.find(class_="sg-score").find(class_="road").find(class_="score").text

	return getFinalScoreMarkdown(home_team, home_team_score, away_team, away_team_score)

def createEmptyThread(home_team, away_team, comp_round, comp_stage, args_info): 
	home_team_parsed = team_info_by_fs.get(home_team).reddit
	away_team_parsed = team_info_by_fs.get(away_team).reddit
 
	title = 'Post-Match Thread: {home_team} - {away_team} [{comp} {comp_stage}, {comp_round}]'.format(comp=args_info.comp_full_name, home_team=home_team_parsed.reddit, away_team=away_team_parsed.reddit, comp_round=comp_round, comp_stage=comp_stage)
	final_markdown = REDDIT_THREAD_PLACEHOLDER_TEXT
	
	submission = el_sub.submit(title=title,selftext=final_markdown)
	flair_choices = submission.flair.choices()

	template_id = next(x for x in flair_choices if x['flair_text'].replace(':','') == args_info.comp_small_name)['flair_template_id']
	submission.flair.select(template_id)
	
	return submission

def getGamesLinks(games_list, args_info):
	r = requests.get(args_info.comp_results_link)
	soup = BeautifulSoup(r.text,'html.parser')

	stage_round_spans = soup.find('div', class_='gc-title').find_all('span')
	comp_stage = stage_round_spans[1].text
	comp_round = stage_round_spans[2].text
	
	all_games_div = soup.find('div', class_='wp-module-asidegames')
	all_game_links = all_games_div.find_all('a', class_='game-link')

	# Possibly change this for a map/list solution if class variable assignments is a thing
	for game in games_list:
		game.game_link = getGameLink(game.home_team, game.away_team, args_info.comp_home_link, all_game_links)
		game.comp_round = comp_round
		game.comp_stage = comp_stage

	return games_list

def getGameLink(home_team, away_team, comp_home_link, all_game_links):
	home_team_parsed = team_info_by_fs.get(home_team)
	away_team_parsed = team_info_by_fs.get(away_team)

	for a_game in all_game_links:
		clubs = a_game.find_all('div', class_='club')
		
		home_club_name = clubs[0].find('span', class_='name').text
		away_club_name = clubs[1].find('span', class_='name').text
		
		if home_team_parsed.official == home_club_name and away_team_parsed.official == away_club_name:
			game_link = comp_home_link + a_game['href']

			return game_link

	return None

def checkIfPageReady(soup):
	# Checks if the top scores panel exists
	return not (soup.find('div', id='ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_gamescorestatic') is None)

# Returns the submission and a boolean representing if the game was updated or not
def updateThread(home_team, away_team, submission, game_link):
	r = requests.get(game_link)
	
	soup = BeautifulSoup(r.text,'html.parser')  
	
	updated = False  

	if checkIfPageReady(soup):
		final_game_information_markdown = getGameInformationMarkdown(soup)
		final_score_markdown = getScoresTable(soup, home_team, away_team)
		final_quarters_score_markdown = getQuarterScoresMarkdown(soup, home_team, away_team)
		home_table_markdown, away_table_markdown = getTablesMarkdown(soup, home_team, away_team)
		
		final_markdown = NEWLINE.join([final_game_information_markdown, REDDIT_HR, final_score_markdown, REDDIT_HR, final_quarters_score_markdown, REDDIT_HR, home_table_markdown, NEWLINE, away_table_markdown])
		
		submission.edit(final_markdown)
		
		updated = True

	return submission, updated

def getTodaysThreads():
	now = datetime.utcnow()# - timedelta(days=30)
	threads = list()
	
	new_submissions = el_sub.new(limit=100)
	
	for submission in new_submissions:
		timestamp = submission.created_utc
		time = datetime.fromtimestamp(timestamp)
	
		# Figure out why it is not possible to break the loop inside the ternary operator
		if time.date() == now.date():
			threads.append(submission)
		else:
			break
		
	return threads

def getTodaysPostGameThreads(comp_full_name):
	todays_threads = getTodaysThreads()
	
	title_regex = r"Post-Match Thread: (.*?)-(.*?)\[" + re.escape(comp_full_name) + r"(.*?)\]"    
	post_game_threads = [(thread, extractThreadTitleInformation(thread.title)) for thread in todays_threads if re.match(title_regex, thread.title)]

	return post_game_threads

def extractThreadTitleInformation(thread_title):
	# Return home_team and away team in Reddit format 
	title_group_regex = r"Post-Match Thread: (?P<home_team>.*?) - (?P<away_team>.*?) \[(?P<competition>(\w+))"
	title_group = re.search(title_group_regex, thread_title)
	
	home_team = findFlashScoreNameByRedditName(title_group.group('home_team').strip())
	away_team = findFlashScoreNameByRedditName(title_group.group('away_team').strip())
	
	return home_team, away_team

def findFlashScoreNameByRedditName(name):
	for fsname in team_info_by_fs.keys():
		other_names = team_info_by_fs[fsname]
		
		if other_names.reddit == name:
			return fsname
		
	return None

if __name__ == '__main__':
	pprint(getTodaysPostGameThreads('EL'))