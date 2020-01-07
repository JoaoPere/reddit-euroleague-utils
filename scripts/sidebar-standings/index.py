import requests
from bs4 import BeautifulSoup
import praw
import sys

CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'

team_names_parsed = dict()

team_names_parsed['CSKA Moscow'] = '[CSKA Moscow](https://www.euroleague.net/competition/teams/showteam?clubcode=CSK&seasoncode=E2019)'
team_names_parsed['Fenerbahce Beko Istanbul'] = '[Fenerbahçe](https://www.euroleague.net/competition/teams/showteam?clubcode=ULK&seasoncode=E2019)'
team_names_parsed['Anadolu Efes Istanbul'] = '[Anadolu Efes](https://www.euroleague.net/competition/teams/showteam?clubcode=IST&seasoncode=E2019)'
team_names_parsed['FC Bayern Munich'] = '[Bayern Munich](https://www.euroleague.net/competition/teams/showteam?clubcode=MUN&seasoncode=E2019)'
team_names_parsed['FC Barcelona'] = '[Barcelona](https://www.euroleague.net/competition/teams/showteam?clubcode=BAR&seasoncode=E2019)'
team_names_parsed['Olympiacos Piraeus'] = '[Olympiacos](https://www.euroleague.net/competition/teams/showteam?clubcode=OLY&seasoncode=E2019)'
team_names_parsed['Khimki Moscow Region'] = '[Khimki](https://www.euroleague.net/competition/teams/showteam?clubcode=KHI&seasoncode=E2019)'
team_names_parsed['Maccabi FOX Tel Aviv'] = '[Maccabi Tel Aviv](https://www.euroleague.net/competition/teams/showteam?clubcode=TEL&seasoncode=E2019)'
team_names_parsed['Zalgiris Kaunas'] = '[Zalgiris Kaunas](https://www.euroleague.net/competition/teams/showteam?clubcode=ZAL&seasoncode=E2019)'
team_names_parsed['KIROLBET Baskonia Vitoria-Gasteiz'] = '[Saski Baskonia](https://www.euroleague.net/competition/teams/showteam?clubcode=BAS&seasoncode=E2019)'
team_names_parsed['Real Madrid'] = '[Real Madrid](https://www.euroleague.net/competition/teams/showteam?clubcode=MAD&seasoncode=E2019)'
team_names_parsed['AX Armani Exchange Milan'] = '[Olimpia Milano](https://www.euroleague.net/competition/teams/showteam?clubcode=MIL&seasoncode=E2019)'
team_names_parsed['Panathinaikos OPAP Athens'] = '[Panathinaikos](https://www.euroleague.net/competition/teams/showteam?clubcode=PAN&seasoncode=E2019)'
team_names_parsed['LDLC ASVEL Villeurbanne'] = '[ASVEL](https://www.euroleague.net/competition/teams/showteam?clubcode=ASV&seasoncode=E2019)'
team_names_parsed['ALBA Berlin'] = '[Alba Berlin](https://www.euroleague.net/competition/teams/showteam?clubcode=BER&seasoncode=E2019)'
team_names_parsed['Valencia Basket'] = '[Valencia](https://www.euroleague.net/competition/teams/showteam?clubcode=PAM&seasoncode=E2019)'
team_names_parsed['Crvena Zvezda mts Belgrade'] = '[Crvena Zvezda](https://www.euroleague.net/competition/teams/showteam?clubcode=RED&seasoncode=E2019)'
team_names_parsed['Zenit St Petersburg'] = '[Zenit](https://www.euroleague.net/competition/teams/showteam?clubcode=DYR&seasoncode=E2019)'

r = requests.get('https://www.euroleague.net/main/standings')

soup = BeautifulSoup(r.text,'html.parser')

def appendTableDelimitors(content):
	return TABLE_DELIM + content + TABLE_DELIM

reddit_table_head = appendTableDelimitors(TABLE_DELIM.join(['#','','W','L','+/-']))
reddit_cell_allignment = appendTableDelimitors(TABLE_DELIM.join([CELL_ALLIGNMENT] * 5))

final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])

# Returns only the standings table
standings_table = soup.find_all("table")

table_rows = standings_table[0].find_all('tr')

for idx, row in enumerate(table_rows[1: len(table_rows)]):
	cols = row.find_all('td')

	# Strips all the leading and trailing white space, removes the digits and shifts the string 2 positions to remove the '. ' substring
	team_name = ''.join([i for i in cols[0].text.strip() if not i.isdigit()])[2:]

	team_markdown = team_names_parsed.get(team_name)

	position = str(idx + 1)
	wins = cols[1].text.strip()
	losses = cols[2].text.strip()
	plus_minus = cols[5].text.strip()

	plus_minus = '+' + plus_minus if plus_minus[0].isdigit() else plus_minus

	cols_markdown = appendTableDelimitors(TABLE_DELIM.join([position, team_markdown, wins, losses, plus_minus]))

	final_table = NEWLINE.join([final_table, cols_markdown])

print(final_table)