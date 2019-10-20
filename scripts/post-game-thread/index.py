import requests
from bs4 import BeautifulSoup
import praw
import sys

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

team_names_parsed = dict()

# Euroleague teams
team_names_parsed['CSKA Moscow'] = 'CSKA Moscow'
team_names_parsed['Fenerbahce Beko Istanbul'] = 'Fenerbahce'
team_names_parsed['Anadolu Efes Istanbul'] = 'Anadolu Efes'
team_names_parsed['FC Bayern Munich'] = 'Bayern Munich'
team_names_parsed['FC Barcelona'] = 'Barcelona'
team_names_parsed['Olympiacos Piraeus'] = 'Olympiacos'
team_names_parsed['Khimki Moscow Region'] = 'Khimki'
team_names_parsed['Maccabi FOX Tel Aviv'] = 'Maccabi Tel Aviv'
team_names_parsed['Zalgiris Kaunas'] = 'Zalgiris Kaunas'
team_names_parsed['KIROLBET Baskonia Vitoria-Gasteiz'] = 'Saski Baskonia'
team_names_parsed['Real Madrid'] = 'Real Madrid'
team_names_parsed['AX Armani Exchange Milan'] = 'Olimpia Milano'
team_names_parsed['Panathinaikos OPAP Athens'] = 'Panathinaikos'
team_names_parsed['LDLC ASVEL Villeurbanne'] = 'ASVEL'
team_names_parsed['ALBA Berlin'] = 'Alba Berlin'
team_names_parsed['Valencia Basket'] = 'Valencia'
team_names_parsed['Crvena Zvezda mts Belgrade'] = 'Crvena Zvezda'
team_names_parsed['Zenit St Petersburg'] = 'Zenit'

#Eurocup teams
team_names_parsed['Tofas Bursa'] = 'Tofas'
team_names_parsed['Darussafaka Tekfen Istanbul'] = 'Darussafaka'
team_names_parsed['Buducnost VOLI Podgorica'] = 'Buducnost'
team_names_parsed['Promitheas Patras'] = 'Promitheas Patras'
team_names_parsed['AS Monaco'] = 'AS Monaco'
team_names_parsed['MoraBanc Andorra'] = 'BC Andorra'
team_names_parsed['ratiopharm Ulm'] = 'ratiopharm Ulm'
team_names_parsed['Segafredo Virtus Bologna'] = 'Virtus Bologna'
team_names_parsed['Maccabi Rishon LeZion'] = 'Maccabi Rishon LeZion'
team_names_parsed['Partizan NIS Belgrade'] = 'Partizan'
team_names_parsed['Lokomotiv Kuban Krasnodar'] = 'Lokomotiv Kuban'
team_names_parsed['Buducnost VOLI Podgorica'] = 'Buducnost'
team_names_parsed['Umana Reyer Venice'] = 'Reyer Venezia'
team_names_parsed['Limoges CSP'] = 'Limoges CSP'
team_names_parsed['Rytas Vilnius'] = 'Rytas'
team_names_parsed['Nanterre 92'] = 'Nanterre 92'
team_names_parsed['Joventut Badalona'] = 'Joventut Badalona'
team_names_parsed['Germani Brescia Leonessa'] = 'Brescia Leonessa'
team_names_parsed['UNICS Kazan'] = 'UNICS Kazan'
team_names_parsed['Cedevita Olimpija Ljubljana'] = 'Cedevita Olimpija Ljubljana'
team_names_parsed['Galatasaray Doga Sigorta Istanbul'] = 'Galatasaray'
team_names_parsed['EWE Baskets Oldenburg'] = 'EWE Baskets Oldenburg'
team_names_parsed['Asseco Arka Gdynia'] = 'Arka Gdynia'
team_names_parsed['Unicaja Malaga'] = 'Unicaja Malaga'
team_names_parsed['Dolomiti Energia Trento'] = 'Aquila Basket Trento'

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

# Formatting table headings
reddit_table_head = appendTableDelimitors(TABLE_DELIM.join([NUMBER, PLAYER, MINUTES, POINTS, FG2, FG3, FREE_TRHOWS, OFF_REBOUNDS, DEF_REBOUNDS, TOT_REBOUNDS, ASSISTS, STEALS, TURNOVERS, BLOCKS, FOULS_COMMITED, PIR]))

# Reddit cell alignment
reddit_cell_allignment = appendTableDelimitors(TABLE_DELIM.join([CELL_ALLIGNMENT] * 16))

home_away_tables = soup.find_all(id='tblPlayerPhaseStatistics')
home_table = home_away_tables[0]
away_table = home_away_tables[1]

home_team_name = team_names_parsed.get(soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_LocalClubStats_lblTeamName").text)
away_team_name = team_names_parsed.get(soup.find(id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_RoadClubStats_lblTeamName").text)

def getTableMarkdown(table):
	table_rows = table.find_all('tr')

	final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])

	for idx, row in enumerate(table_rows[2: len(table_rows) - 1]):
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]

		# Removes the blocks against and fouls drawn columns
		cols.pop(16)
		cols.pop(14)

		cols_markdown = appendTableDelimitors(TABLE_DELIM.join(cols))
		final_table = NEWLINE.join([final_table, cols_markdown])

		if (idx+2) == (len(table_rows) - 2):
			score = int(cols[3])

	return final_table, score

home_table_markdown, home_team_score = getTableMarkdown(home_table)
away_table_markdown, away_team_score = getTableMarkdown(away_table)

final_markdown = NEWLINE.join([home_table_markdown, NEWLINE, away_table_markdown])

game_info_div = soup.find('div', class_='gc-title')
game_info_spans = game_info_div.find_all('span')

game_info_spans = list(map(lambda gi: gi.text.strip(), game_info_spans))

stage = game_info_spans[2]

title = 'Post-Match Thread: {home_team} - {away_team} [{comp}, {stage}]'.format(comp=competition, home_team=home_team_name, away_team=away_team_name, stage=stage)

print('-------------------------------')
print(title)
print('-------------------------------')
print(final_markdown)
print('-------------------------------')

reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
                     client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
                     password='tQ#1O&4k32Xy',
                     user_agent='Euroleague Post-Game Thread Script',
                     username='Al-Farrekt-Aminu')

el_sub = reddit.subreddit('Euroleague')

el_sub.submit(title=title,
			  selftext=final_markdown)