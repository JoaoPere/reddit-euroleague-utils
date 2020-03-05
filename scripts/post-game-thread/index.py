import requests
from bs4 import BeautifulSoup
import praw
import sys
from pprint import pprint
import smart_open.smart_open_lib
import os

sys.path.append('..')

from team_structs import team_info_by_official
from prepare_dot_env import prepareDotEnv

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

CELL_ALLIGNMENT = ':-'

if sys.argv[1] == 'EL':
	r = requests.get('https://www.euroleague.net/main/results/showgame?gamecode={}&seasoncode=E2019'.format(sys.argv[2]))
	competition = 'EuroLeague'
elif sys.argv[1] == 'EC':
	r = requests.get('https://www.eurocupbasketball.com/eurocup/games/results/showgame?gamecode={}&seasoncode=U2019'.format(sys.argv[2]))
	competition = 'EuroCup'

soup = BeautifulSoup(r.text,'html.parser')

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

def getQuarterScoresMarkdown():
	quarter_table = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_PartialsStatsByQuarter_dgPartials")
	quarter_table_rows = quarter_table.find_all('tr')

	table_head_elements = [th.text.upper() for th in quarter_table_rows[0].find_all('th')]
	final_table = getRedditTableHeadAndCellAlignment(table_head_elements)

	for idx, row in enumerate(quarter_table_rows[1:]):
		quarter_table_cols = row.find_all('td')
		quarter_table_cols = [ele.text.strip() for ele in quarter_table_cols]

		# Overrides the team name
		quarter_table_cols[0] = team_info_by_official.get(quarter_table_cols[0]).full_md

		cols_markdown = appendTableDelimitors(TABLE_DELIM.join(quarter_table_cols))

		final_table = NEWLINE.join([final_table, cols_markdown])

	return final_table

def getTablesMarkdown(home_team_name, away_team_name):
	home_away_tables = soup.find_all(id='tblPlayerPhaseStatistics')
	home_table = home_away_tables[0]
	away_table = home_away_tables[1]

	home_coach = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_LocalClubStats_lblHeadCoach").text
	away_coach = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_RoadClubStats_lblHeadCoach").text

	return getTableMarkdown(home_table, home_team_name, home_coach), getTableMarkdown(away_table, away_team_name, away_coach)

def getTableMarkdown(table, name, coach):
	table_rows = table.find_all('tr')

	TEAM_MD = team_info_by_official.get(name).full_md.upper()

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

	home_team_md = team_info_by_official.get(home_team_name).full_md
	away_team_md = team_info_by_official.get(away_team_name).full_md

	home_team_name_score = appendTableDelimitors(TABLE_DELIM.join([home_team_md, home_team_score]))
	away_team_name_score = appendTableDelimitors(TABLE_DELIM.join([away_team_md, away_team_score]))


	final_table = NEWLINE.join([final_table, home_team_name_score, away_team_name_score])

	return final_table

def getGameInformationMarkdown():
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

def getTeamNamesAndScoresTable():
	home_team_orig = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_LocalClubStats_lblTeamName").text
	away_team_orig = soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_RoadClubStats_lblTeamName").text

	home_team_name = team_info_by_official.get(home_team_orig).reddit
	away_team_name = team_info_by_official.get(away_team_orig).reddit

	home_team_score = soup.find(class_="sg-score").find(class_="local").find(class_="score").text
	away_team_score = soup.find(class_="sg-score").find(class_="road").find(class_="score").text

	return home_team_orig, home_team_name, away_team_orig, away_team_name, getFinalScoreMarkdown(home_team_orig, home_team_score, away_team_orig, away_team_score)

def getGameStage():
	game_info_div = soup.find('div', class_='gc-title')
	game_info_spans = game_info_div.find_all('span')

	game_info_spans = list(map(lambda gi: gi.text.strip(), game_info_spans))

	comp_stage = game_info_spans[1]
	comp_round = game_info_spans[2]

	return comp_stage, comp_round

if __name__ == '__main__':
	prepareDotEnv()

	final_game_information_markdown = getGameInformationMarkdown()
	home_team_orig, home_team_name, away_team_orig, away_team_name, final_score_markdown = getTeamNamesAndScoresTable()
	final_quarters_score_markdown = getQuarterScoresMarkdown()
	home_table_markdown, away_table_markdown = getTablesMarkdown(home_team_orig, away_team_orig)
	comp_stage, comp_round = getGameStage()

	final_markdown = NEWLINE.join([final_game_information_markdown, REDDIT_HR, final_score_markdown, REDDIT_HR, final_quarters_score_markdown, REDDIT_HR, home_table_markdown, NEWLINE, away_table_markdown])

	title = 'Post-Match Thread: {home_team} - {away_team} [{comp} {comp_stage}, {comp_round}]'.format(comp=competition, home_team=home_team_name, away_team=away_team_name, comp_round= comp_round, comp_stage=comp_stage)

	reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
						client_secret=os.getenv("REDDIT_APP_SECRET"),
						password=os.getenv("REDDIT_PASSWORD"),
						username=os.getenv("REDDIT_ACCOUNT"),
						user_agent="r/EuroLeague Post Game Thread Generator Script")

	el_sub = reddit.subreddit('Euroleague')

	submission = el_sub.submit(title=title,selftext=final_markdown)

	flair_choices = submission.flair.choices()

	template_id = next(x for x in flair_choices if x['flair_text'].replace(':','') == sys.argv[1])['flair_template_id']
	submission.flair.select(template_id)