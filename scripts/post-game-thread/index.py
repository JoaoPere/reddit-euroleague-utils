import requests
from bs4 import BeautifulSoup
import praw
import sys
from pprint import pprint

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


team_names_parsed_link_3 = dict()

team_names_parsed_link_3['CSKA Moscow'] = '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)'
team_names_parsed_link_3['Fenerbahce Beko Istanbul'] = '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)'
team_names_parsed_link_3['Anadolu Efes Istanbul'] = '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)'
team_names_parsed_link_3['FC Bayern Munich'] = '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)'
team_names_parsed_link_3['FC Barcelona'] = '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)'
team_names_parsed_link_3['Olympiacos Piraeus'] = '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)'
team_names_parsed_link_3['Khimki Moscow Region'] = '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)'
team_names_parsed_link_3['Maccabi FOX Tel Aviv'] = '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)'
team_names_parsed_link_3['Zalgiris Kaunas'] = '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)'
team_names_parsed_link_3['KIROLBET Baskonia Vitoria-Gasteiz'] = '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)'
team_names_parsed_link_3['Real Madrid'] = '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)'
team_names_parsed_link_3['AX Armani Exchange Milan'] = '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)'
team_names_parsed_link_3['Panathinaikos OPAP Athens'] = '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)'
team_names_parsed_link_3['LDLC ASVEL Villeurbanne'] = '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)'
team_names_parsed_link_3['ALBA Berlin'] = '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)'
team_names_parsed_link_3['Valencia Basket'] = '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)'
team_names_parsed_link_3['Crvena Zvezda mts Belgrade'] = '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)'
team_names_parsed_link_3['Zenit St Petersburg'] = '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)'

team_names_parsed_link_3['Tofas Bursa'] = '[TOF](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)'
team_names_parsed_link_3['Darussafaka Tekfen Istanbul'] = '[DTI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)'
team_names_parsed_link_3['Buducnost VOLI Podgorica'] = '[BUD](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)'
team_names_parsed_link_3['Promitheas Patras'] = '[PRO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)'
team_names_parsed_link_3['AS Monaco'] = '[MON](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)'
team_names_parsed_link_3['MoraBanc Andorra'] = '[MBA](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)'
team_names_parsed_link_3['ratiopharm Ulm'] = '[ULM](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)'
team_names_parsed_link_3['Segafredo Virtus Bologna'] = '[VIR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)'
team_names_parsed_link_3['Maccabi Rishon LeZion'] = '[RLZ](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)'
team_names_parsed_link_3['Partizan NIS Belgrade'] = '[PAR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)'
team_names_parsed_link_3['Lokomotiv Kuban Krasnodar'] = '[LOK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)'
team_names_parsed_link_3['Umana Reyer Venice'] = '[URV](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)'
team_names_parsed_link_3['Limoges CSP'] = '[CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)'
team_names_parsed_link_3['Rytas Vilnius'] = '[RYT](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)'
team_names_parsed_link_3['Nanterre 92'] = '[NTR](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)'
team_names_parsed_link_3['Joventut Badalona'] = '[CJB](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)'
team_names_parsed_link_3['Germani Brescia Leonessa'] = '[BRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)'
team_names_parsed_link_3['UNICS Kazan'] = '[UNK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)'
team_names_parsed_link_3['Cedevita Olimpija Ljubljana'] = '[COL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)'
team_names_parsed_link_3['Galatasaray Doga Sigorta Istanbul'] = '[GAL](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)'
team_names_parsed_link_3['EWE Baskets Oldenburg'] = '[EBO](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)'
team_names_parsed_link_3['Asseco Arka Gdynia'] = '[ARK](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)'
team_names_parsed_link_3['Unicaja Malaga'] = '[UNI](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)'
team_names_parsed_link_3['Dolomiti Energia Trento'] = '[TRE](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)'

team_names_parsed_link_full = dict()

team_names_parsed_link_full['CSKA Moscow'] = '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)'
team_names_parsed_link_full['Fenerbahce Beko Istanbul'] = '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)'
team_names_parsed_link_full['Anadolu Efes Istanbul'] = '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)'
team_names_parsed_link_full['FC Bayern Munich'] = '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)'
team_names_parsed_link_full['FC Barcelona'] = '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)'
team_names_parsed_link_full['Olympiacos Piraeus'] = '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)'
team_names_parsed_link_full['Khimki Moscow Region'] = '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)'
team_names_parsed_link_full['Maccabi FOX Tel Aviv'] = '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)'
team_names_parsed_link_full['Zalgiris Kaunas'] = '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)'
team_names_parsed_link_full['KIROLBET Baskonia Vitoria-Gasteiz'] = '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)'
team_names_parsed_link_full['Real Madrid'] = '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)'
team_names_parsed_link_full['AX Armani Exchange Milan'] = '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)'
team_names_parsed_link_full['Panathinaikos OPAP Athens'] = '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)'
team_names_parsed_link_full['LDLC ASVEL Villeurbanne'] = '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)'
team_names_parsed_link_full['ALBA Berlin'] = '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)'
team_names_parsed_link_full['Valencia Basket'] = '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)'
team_names_parsed_link_full['Crvena Zvezda mts Belgrade'] = '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)'
team_names_parsed_link_full['Zenit St Petersburg'] = '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)'

team_names_parsed_link_full['Tofas Bursa'] = '[Tofas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUR&seasoncode=U2019)'
team_names_parsed_link_full['Darussafaka Tekfen Istanbul'] = '[Darussafaka](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=DAR&seasoncode=U2019)'
team_names_parsed_link_full['Buducnost VOLI Podgorica'] = '[Buducnost](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BUD&seasoncode=U2019)'
team_names_parsed_link_full['Promitheas Patras'] = '[Promitheas Patras](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAT&seasoncode=U2019)'
team_names_parsed_link_full['AS Monaco'] = '[AS Monaco](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MCO&seasoncode=U2019)'
team_names_parsed_link_full['MoraBanc Andorra'] = '[BC Andorra](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ANR&seasoncode=U2019)'
team_names_parsed_link_full['ratiopharm Ulm'] = '[ratiopharm Ulm](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=ULM&seasoncode=U2019)'
team_names_parsed_link_full['Segafredo Virtus Bologna'] = '[Virtus Bologna](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VIR&seasoncode=U2019)'
team_names_parsed_link_full['Maccabi Rishon LeZion'] = '[Maccabi Rishon LeZion](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=RIS&seasoncode=U2019)'
team_names_parsed_link_full['Partizan NIS Belgrade'] = '[Partizan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=PAR&seasoncode=U2019)'
team_names_parsed_link_full['Lokomotiv Kuban Krasnodar'] = '[Lokomotiv Kuban](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TIV&seasoncode=U2019)'
team_names_parsed_link_full['Umana Reyer Venice'] = '[Reyer Venezia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=VNC&seasoncode=U2019)'
team_names_parsed_link_full['Limoges CSP'] = '[Limoges CSP](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LMG&seasoncode=U2019)'
team_names_parsed_link_full['Rytas Vilnius'] = '[Rytas](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LIE&seasoncode=U2019)'
team_names_parsed_link_full['Nanterre 92'] = '[Nanterre 92](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=NTR&seasoncode=U2019)'
team_names_parsed_link_full['Joventut Badalona'] = '[Joventut Badalona](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=JOV&seasoncode=U2019)'
team_names_parsed_link_full['Germani Brescia Leonessa'] = '[Brescia Leonessa](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=BRE&seasoncode=U2019)'
team_names_parsed_link_full['UNICS Kazan'] = '[UNICS Kazan](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=UNK&seasoncode=U2019)'
team_names_parsed_link_full['Cedevita Olimpija Ljubljana'] = '[Cedevita Olimpija Ljubljana](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=LJU&seasoncode=U2019)'
team_names_parsed_link_full['Galatasaray Doga Sigorta Istanbul'] = '[Galatasaray](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=GAL&seasoncode=U2019)'
team_names_parsed_link_full['EWE Baskets Oldenburg'] = '[EWE Baskets Oldenburg](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=OLD&seasoncode=U2019)'
team_names_parsed_link_full['Asseco Arka Gdynia'] = '[Arka Gdynia](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=SOP&seasoncode=U2019)'
team_names_parsed_link_full['Unicaja Malaga'] = '[Unicaja Malaga](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=MAL&seasoncode=U2019)'
team_names_parsed_link_full['Dolomiti Energia Trento'] = '[Aquila Basket Trento](https://www.eurocupbasketball.com/eurocup/competition/teams/showteam?clubcode=TRN&seasoncode=U2019)'


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

	final_table = getRedditTableHeadAndCellAlignment(['BY QUARTER','1','2','3','4'])

	for idx, row in enumerate(quarter_table_rows[1:]):
		quarter_table_cols = row.find_all('td')
		quarter_table_cols = [ele.text.strip() for ele in quarter_table_cols]

		# Overrides the team name
		quarter_table_cols[0] = team_names_parsed_link_full.get(quarter_table_cols[0])

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

	TEAM_MD = team_names_parsed_link_full.get(name).upper()

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

	home_team_md = team_names_parsed_link_full.get(home_team_name)
	away_team_md = team_names_parsed_link_full.get(away_team_name)

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

	home_team_name = team_names_parsed.get(home_team_orig)
	away_team_name = team_names_parsed.get(away_team_orig)

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

final_game_information_markdown = getGameInformationMarkdown()
home_team_orig, home_team_name, away_team_orig, away_team_name, final_score_markdown = getTeamNamesAndScoresTable()
final_quarters_score_markdown = getQuarterScoresMarkdown()
home_table_markdown, away_table_markdown = getTablesMarkdown(home_team_orig, away_team_orig)
comp_stage, comp_round = getGameStage()

final_markdown = NEWLINE.join([final_game_information_markdown, REDDIT_HR, final_score_markdown, REDDIT_HR, final_quarters_score_markdown, REDDIT_HR, home_table_markdown, NEWLINE, away_table_markdown])

title = 'Post-Match Thread: {home_team} - {away_team} [{comp} {comp_stage}, {comp_round}]'.format(comp=competition, home_team=home_team_name, away_team=away_team_name, comp_round= comp_round, comp_stage=comp_stage)

reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
                     client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
                     password='tQ#1O&4k32Xy',
                     user_agent='Euroleague Post-Game Thread Script',
                     username='Al-Farrekt-Aminu')

el_sub = reddit.subreddit('Euroleague')

submission = el_sub.submit(title=title,selftext=final_markdown)

flair_choices = submission.flair.choices()

pprint(flair_choices)
template_id = next(x for x in flair_choices if x['flair_text'].replace(':','') == sys.argv[1])['flair_template_id']
submission.flair.select(template_id)

print("*" * 119)
print(title)
print("*" * 119)
print(final_markdown)
print("*" * 119)

print("Successfully published thread")