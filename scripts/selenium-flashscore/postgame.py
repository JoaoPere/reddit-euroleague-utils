import requests
from bs4 import BeautifulSoup
import praw
from pprint import pprint
from collections import namedtuple
from datetime import datetime, timedelta
import re
import sys
from requests.adapters import HTTPAdapter

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

teams_flashscore_parsed = dict()
TeamNameParsed = namedtuple('TeamNameParsed', 'official reddit letter3_md full_md')

teams_flashscore_parsed['CSKA Moscow'] = TeamNameParsed('CSKA Moscow', 'CSKA Moscow', '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)', '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)')
teams_flashscore_parsed['Fenerbahce'] = TeamNameParsed('Fenerbahce Beko Istanbul', 'Fenerbahce', '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)', '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)')
teams_flashscore_parsed['Anadolu Efes'] = TeamNameParsed('Anadolu Efes Istanbul', 'Anadolu Efes', '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)', '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)')
teams_flashscore_parsed['Bayern'] = TeamNameParsed('FC Bayern Munich', 'Bayern Munich', '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)', '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)')
teams_flashscore_parsed['Barcelona'] = TeamNameParsed('FC Barcelona', 'Barcelona', '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)', '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)')
teams_flashscore_parsed['Olympiacos'] = TeamNameParsed('Olympiacos Piraeus', 'Olympiacos', '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)', '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)')
teams_flashscore_parsed['Khimki M.'] = TeamNameParsed('Khimki Moscow Region', 'Khimki', '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)', '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)')
teams_flashscore_parsed['Maccabi Tel Aviv'] = TeamNameParsed('Maccabi FOX Tel Aviv', 'Maccabi Tel Aviv', '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)', '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)')
teams_flashscore_parsed['Zalgiris Kaunas'] = TeamNameParsed('Zalgiris Kaunas', 'Zalgiris Kaunas', '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)', '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)')
teams_flashscore_parsed['Baskonia'] = TeamNameParsed('KIROLBET Baskonia Vitoria-Gasteiz', 'Saski Baskonia', '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)', '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)')
teams_flashscore_parsed['Real Madrid'] = TeamNameParsed('Real Madrid', 'Real Madrid', '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)', '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)')
teams_flashscore_parsed['Olimpia Milano'] = TeamNameParsed('AX Armani Exchange Milan', 'Olimpia Milano', '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)', '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)')
teams_flashscore_parsed['Panathinaikos'] = TeamNameParsed('Panathinaikos OPAP Athens', 'Panathinaikos', '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)', '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)')
teams_flashscore_parsed['Lyon-Villeurbanne'] = TeamNameParsed('LDLC ASVEL Villeurbanne', 'ASVEL', '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)', '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)')
teams_flashscore_parsed['Alba Berlin'] = TeamNameParsed('ALBA Berlin', 'Alba Berlin', '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)', '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)')
teams_flashscore_parsed['Valencia'] = TeamNameParsed('Valencia Basket', 'Valencia', '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)', '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)')
teams_flashscore_parsed['Crvena zvezda mts'] = TeamNameParsed('Crvena Zvezda mts Belgrade', 'Crvena Zvezda', '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)', '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)')
teams_flashscore_parsed['Zenit Petersburg'] = TeamNameParsed('Zenit St Petersburg', 'Zenit', '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)', '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)')

#Eurocup teams
teams_flashscore_parsed['Tofas'] = TeamNameParsed('Tofas Bursa', 'Tofas', '[TOF](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)', '[Tofas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)')
teams_flashscore_parsed['Darussafaka'] = TeamNameParsed('Darussafaka Tekfen Istanbul','Darussafaka', '[DTI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)', '[Darussafaka](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)')
teams_flashscore_parsed['Buducnost'] = TeamNameParsed('Buducnost VOLI Podgorica', 'Buducnost', '[BUD](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)', '[Buducnost](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)')
teams_flashscore_parsed['Promitheas'] = TeamNameParsed('Promitheas Patras', 'Promitheas Patras', '[PRO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)', '[Promitheas Patras](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)')
teams_flashscore_parsed['Monaco'] = TeamNameParsed('AS Monaco', 'AS Monaco', '[MON](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)', '[AS Monaco](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)')
teams_flashscore_parsed['MoraBanc Andorra'] = TeamNameParsed('MoraBanc Andorra','BC Andorra', '[MBA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)', '[BC Andorra](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)')
teams_flashscore_parsed['Ulm'] = TeamNameParsed('ratiopharm Ulm', 'ratiopharm Ulm', '[ULM](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)', '[ratiopharm Ulm](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)')
teams_flashscore_parsed['Virtus Bologna'] = TeamNameParsed('Segafredo Virtus Bologna','Virtus Bologna', '[VIR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)', '[Virtus Bologna](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)')
teams_flashscore_parsed['Maccabi Rishon'] = TeamNameParsed('Maccabi Rishon LeZion', 'Maccabi Rishon LeZion', '[RLZ](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)', '[Maccabi Rishon LeZion](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)')
teams_flashscore_parsed['Partizan'] = TeamNameParsed('Partizan NIS Belgrade', 'Partizan', '[PAR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)', '[Partizan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)')
teams_flashscore_parsed['Lokomotiv Kuban'] = TeamNameParsed('Lokomotiv Kuban Krasnodar', 'Lokomotiv Kuban', '[LOK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)', '[Lokomotiv Kuban](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)')
teams_flashscore_parsed['Venezia'] = TeamNameParsed('Umana Reyer Venice', 'Reyer Venezia', '[URV](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)', '[Reyer Venezia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)')
teams_flashscore_parsed['Limoges'] = TeamNameParsed('Limoges CSP', 'Limoges CSP', '[CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)', '[Limoges CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)')
teams_flashscore_parsed['Rytas'] = TeamNameParsed('Rytas Vilnius', 'Rytas', '[RYT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)', '[Rytas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)')
teams_flashscore_parsed['Nanterre'] = TeamNameParsed('Nanterre 92', 'Nanterre 92', '[NTR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)', '[Nanterre 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)')
teams_flashscore_parsed['Joventut Badalona'] = TeamNameParsed('Joventut Badalona', 'Joventut Badalona', '[CJB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)', '[Joventut Badalona](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)')
teams_flashscore_parsed['Brescia'] = TeamNameParsed('Germani Brescia Leonessa','Brescia Leonessa', '[BRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)', '[Brescia Leonessa](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)')
teams_flashscore_parsed['Unics Kazan'] = TeamNameParsed('UNICS Kazan', 'UNICS Kazan', '[UNK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)', '[UNICS Kazan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)')
teams_flashscore_parsed['Cedevita Olimpija'] = TeamNameParsed('Cedevita Olimpija Ljubljana', 'Cedevita Olimpija Ljubljana', '[COL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)', '[Cedevita Olimpija Ljubljana](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)')
teams_flashscore_parsed['Galatasaray'] = TeamNameParsed('Galatasaray Doga Sigorta Istanbul', 'Galatasaray', '[GAL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)', '[Galatasaray](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)')
teams_flashscore_parsed['Oldenburg'] = TeamNameParsed('EWE Baskets Oldenburg', 'EWE Baskets Oldenburg', '[EBO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)', '[EWE Baskets Oldenburg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)')
teams_flashscore_parsed['Gdynia'] = TeamNameParsed('Asseco Arka Gdynia', 'Arka Gdynia', '[ARK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)', '[Arka Gdynia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)')
teams_flashscore_parsed['Unicaja'] = TeamNameParsed('Unicaja Malaga', 'Unicaja Malaga', '[UNI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)', '[Unicaja Malaga](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)')
teams_flashscore_parsed['Trento'] = TeamNameParsed('Dolomiti Energia Trento', 'Aquila Basket Trento', '[TRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)', '[Aquila Basket Trento](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)')

CELL_ALLIGNMENT = ':-'

reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
					 client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
					 password='tQ#1O&4k32Xy',
					 user_agent='Euroleague Post-Game Thread Script',
					 username='Al-Farrekt-Aminu')

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
		quarter_table_cols[0] = teams_flashscore_parsed.get(home_team).full_md if idx == 0 else teams_flashscore_parsed.get(away_team).full_md

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

	TEAM_MD = teams_flashscore_parsed.get(name).full_md.upper()

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

	home_team_md = teams_flashscore_parsed.get(home_team_name).full_md
	away_team_md = teams_flashscore_parsed.get(away_team_name).full_md

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

def createEmptyThread(home_team, away_team, args_info): 
	home_team_parsed = teams_flashscore_parsed.get(home_team)
	away_team_parsed = teams_flashscore_parsed.get(away_team)
 
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

	return games_list

def getGameLink(home_team, away_team, comp_home_link, all_game_links):
	home_team_parsed = teams_flashscore_parsed.get(home_team)
	away_team_parsed = teams_flashscore_parsed.get(away_team)

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
	for fsname in teams_flashscore_parsed.keys():
		other_names = teams_flashscore_parsed[fsname]
		
		if other_names.reddit == name:
			return fsname
		
	return None

if __name__ == '__main__':
	pprint(getTodaysPostGameThreads('EL'))