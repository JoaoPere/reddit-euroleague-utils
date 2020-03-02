import requests
from bs4 import BeautifulSoup
import sys
from collections import namedtuple
from datetime import datetime, timezone, tzinfo
import praw

CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'

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

def appendTableDelimitors(content):
	return TABLE_DELIM + content + TABLE_DELIM

# TODO: Rename this
def findOtherValueByValue(search_index, search_condition, result_index):            
	for value in teams_flashscore_parsed.values(): 
		if value[search_index] == search_condition:
			return value[result_index]
		
	return None
   
# Returns the href to the result thread 
# For now, only covering regular season  
def getResultThread(home_team, away_team, el_round):
	reddit_home_team = findOtherValueByValue(0, home_team, 1)
	reddit_away_team = findOtherValueByValue(0, away_team, 1)
	
	reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
		client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
			  password='tQ#1O&4k32Xy',
					   user_agent='Euroleague Post-Game Thread Script',
								   username='Al-Farrekt-Aminu')
	
	el_sub = reddit.subreddit('Euroleague')
	new_submissions = el_sub.new(limit=100)
	
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
	
	for idx, html_game in enumerate(schedule_html_games):
		both_clubs = html_game.find_all("div", class_="club")
		
		home_team_official = both_clubs[0].find("span", class_="name").text
		away_team_official = both_clubs[1].find("span", class_="name").text
		
		home_team_name = findOtherValueByValue(0, home_team_official, 2)
		home_team_score = both_clubs[0].find("span", class_="score").attrs['data-score']
	
		away_team_name = findOtherValueByValue(0, away_team_official, 2)
		away_team_score = both_clubs[1].find("span", class_="score").attrs['data-score']
	
		# Only assign to the first row of the table - Reddit markdown syntax related
		el_round = str(week) if idx == 0 else ""
		
		submission_url = getResultThread(home_team_official, away_team_official, str(week))
		
		result = "[{home_team_score}-{away_team_score}]({submission_url})".format(home_team_score=home_team_score, away_team_score=away_team_score,submission_url=submission_url)
	
		row_markdown = appendTableDelimitors(TABLE_DELIM.join([el_round, home_team_name, away_team_name, result]))
	
		final_table = NEWLINE.join([final_table, row_markdown])
		
	final_table = NEWLINE.join([final_table, '**Note:** Access the post-match threads by clicking in the result'])
	
	return final_table

if __name__ == '__main__':
	print(getResultsTable(sys.argv[1]))