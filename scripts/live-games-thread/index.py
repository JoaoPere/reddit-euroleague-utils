from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import praw
from collections import namedtuple

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

DOUBLE_NEWLINE = '\n\n'

# Perhaps look into refactoring both functions into one and/or refactor some common operations between both
def getEuroCupGames(now_time, soup):
	group_container = soup.find_all('div', class_='group-container')
	games_markdown = list()

	for group in group_container:
		group_name = group.find('div', class_='group').text

		group_games = group.find_all('div', class_='game')		

		for game in group_games:
			game_date = game.find('span', class_='date')

			# Date is not set, continue to next game
			if game_date is None:
				continue
			
			game_date = game_date.text

			game_date = game_date.strip()[:len(game_date) - 4]
			game_date = datetime.strptime(game_date, "%B %d %H:%M")

			if game_date.day == now_time.day and game_date.month == now_time.month:
				game_clubs = game.find_all('div',class_='club')

				game_home_team = team_names_parsed.get(game_clubs[0].find('span', class_='name').text)
				game_away_team = team_names_parsed.get(game_clubs[1].find('span', class_='name').text)

				game_md = "{home_team} - {away_team} | {hours}:{minutes} CET  | {group_name}".format(home_team=bold(game_home_team), away_team=bold(game_away_team), hours=game_date.strftime('%H'), minutes=game_date.strftime('%M'), group_name=group_name)

				games_markdown.append((game_date,game_md))

		games_markdown.sort(key=lambda d: d[0])
	
	return games_markdown

def getEuroLeagueGames(now_time, soup):
	all_games = soup.find_all('div', class_='livescore')[1].find_all('div', class_='game')

	games_markdown = list()

	for game in all_games:
		game_date = game.find('span', class_='date').text

		game_date = game_date.strip()[:len(game_date) - 4]
		game_date = datetime.strptime(game_date, "%B %d %H:%M")

		# Date is not set, continue to next game
		if game_date is None:
			continue

		if game_date.day == now_time.day and game_date.month == now_time.month:
			game_clubs = game.find_all('div',class_='club')

			game_home_team = team_names_parsed.get(game_clubs[0].find('span', class_='name').text)
			game_away_team = team_names_parsed.get(game_clubs[1].find('span', class_='name').text)

			game_md = "{home_team} - {away_team} | {hours}:{minutes} CET".format(home_team=bold(game_home_team), away_team=bold(game_away_team), hours=game_date.strftime('%H'), minutes=game_date.strftime('%M'))
			games_markdown.append((game_date,game_md))

	return games_markdown

def bold(text):
	return '**' + text + '**'

if __name__ == '__main__':
	ArgsParseTuple = namedtuple('ArgsParseTuple', 'results_url comp_full_name comp_small_name markdown_function')
	args_dict = dict()
	
	args_dict['EL'] = ArgsParseTuple('https://www.euroleague.net/main/results', 'EuroLeague', 'EL', getEuroLeagueGames)
	args_dict['EC'] = ArgsParseTuple('https://www.eurocupbasketball.com/eurocup/games/results', 'EuroCup', 'EC', getEuroCupGames)
	
	if(sys.argv[1] not in args_dict):
		sys.exit()
		
	args_info = args_dict.get(sys.argv[1])

	now_time = datetime.now()
	r = requests.get(args_info.results_url)
	soup = BeautifulSoup(r.text,'html.parser')

	games_markdown = args_info.markdown_function(now_time, soup)
	final_markdown = DOUBLE_NEWLINE.join([*(list(zip(*games_markdown))[1]),  'You can ask for and share streams in the comments here, do not submit separate threads about streaming please.'])
	final_title = "{today_date} {competition} Matches Live Thread".format(today_date=now_time.strftime('%d %B %Y'), competition=args_info.comp_full_name)

	reddit = praw.Reddit(client_id='Qbl7w1uV9945aw',
						client_secret='a8S1qsebIhlWQyPrVTHp0mH5dAA',
						password='tQ#1O&4k32Xy',
						user_agent='Euroleague Live Game Thread Script',
						username='Al-Farrekt-Aminu')

	el_sub = reddit.subreddit('Euroleague')

	submission = el_sub.submit(title=final_title,selftext=final_markdown)
	submission.mod.sticky()
	submission.mod.suggested_sort('new')

	flair_choices = submission.flair.choices()
	template_id = next(x for x in flair_choices if x['flair_text'].replace(':','') == args_info.comp_small_name)['flair_template_id']
	submission.flair.select(template_id)