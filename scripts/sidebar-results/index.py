import requests
from bs4 import BeautifulSoup
import praw
import sys
from datetime import datetime, timezone, tzinfo

CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'

team_names_parsed = dict()

team_names_parsed['CSKA Moscow'] = '[CSK](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)'
team_names_parsed['Fenerbahce Beko Istanbul'] = '[FNB](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)'
team_names_parsed['Anadolu Efes Istanbul'] = '[EFS](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)'
team_names_parsed['FC Bayern Munich'] = '[BAY](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)'
team_names_parsed['FC Barcelona'] = '[BAR](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)'
team_names_parsed['Olympiacos Piraeus'] = '[OLY](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)'
team_names_parsed['Khimki Moscow Region'] = '[KHI](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)'
team_names_parsed['Maccabi FOX Tel Aviv'] = '[MTA](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)'
team_names_parsed['Zalgiris Kaunas'] = '[ZAL](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)'
team_names_parsed['KIROLBET Baskonia Vitoria-Gasteiz'] = '[KBA](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)'
team_names_parsed['Real Madrid'] = '[RMA](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)'
team_names_parsed['AX Armani Exchange Milan'] = '[MIL](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)'
team_names_parsed['Panathinaikos OPAP Athens'] = '[PAO](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)'
team_names_parsed['LDLC ASVEL Villeurbanne'] = '[ASV](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)'
team_names_parsed['ALBA Berlin'] = '[BER](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)'
team_names_parsed['Valencia Basket'] = '[VBC](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)'
team_names_parsed['Crvena Zvezda mts Belgrade'] = '[CZV](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)'
team_names_parsed['Zenit St Petersburg'] = '[ZEN](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)'


def appendTableDelimitors(content):
	return TABLE_DELIM + content + TABLE_DELIM

# TODO: Add support to playoffs
def getResultsTable():
	r = requests.get('https://www.euroleague.net/main/results?gamenumber={}&phasetypecode=RS&seasoncode=E2019'.format(sys.argv[1]))
	
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
		
		home_team_name = team_names_parsed.get(str(both_clubs[0].find("span", class_="name").get_text()))
		home_team_score = both_clubs[0].find("span", class_="score").attrs['data-score']
	
		away_team_name = team_names_parsed.get(str(both_clubs[1].find("span", class_="name").get_text()))
		away_team_score = both_clubs[1].find("span", class_="score").attrs['data-score']
	
		el_round = sys.argv[1] if idx == 0 else ""
		result = "[{}-{}]()".format(home_team_score, away_team_score)
	
		row_markdown = appendTableDelimitors(TABLE_DELIM.join([el_round, home_team_name, away_team_name, result]))
	
		final_table = NEWLINE.join([final_table, row_markdown])
	
	return final_table

if __name__ == '__main__':
	print(getResultsTable())