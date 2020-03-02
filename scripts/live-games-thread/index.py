from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import praw

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

now_time = datetime.now()

def bold(text):
	return '**' + text + '**'

if sys.argv[1] == 'EL':
	r = requests.get('https://www.euroleague.net/main/results')
	comp = 'EuroLeague'
elif sys.argv[1] == 'EC':
	r = requests.get('https://www.eurocupbasketball.com/eurocup/games/results')
	comp = 'EuroCup'

soup = BeautifulSoup(r.text,'html.parser')

all_games = soup.find_all('div', class_='livescore')[1].find_all('div', class_='game')

games_markdown = list()

for game in all_games:
	game_date = game.find('span', class_='date').text

	game_date = game_date.strip()[:len(game_date) - 4]
	game_date = datetime.strptime(game_date, "%B %d %H:%M")

	if game_date.day == now_time.day and game_date.month == now_time.month:
		game_clubs = game.find_all('div',class_='club')

		game_home_team = team_names_parsed.get(game_clubs[0].find('span', class_='name').text)
		game_away_team = team_names_parsed.get(game_clubs[1].find('span', class_='name').text)

		game_md = bold(game_home_team) + ' - ' + bold(game_away_team) + ' | ' + game_date.strftime('%H') + ':' + game_date.strftime('%M') + ' CET'
		if sys.argv[1] == 'EC':
			game_md = game_md + ' | Group '

		games_markdown.append(game_md)

final_markdown = DOUBLE_NEWLINE.join([*games_markdown,  'You can ask for and share streams in the comments here, do not submit separate threads about streaming please.'])
final_title = now_time.strftime('%d %B %Y') + ' ' + comp + ' Matches Live Thread'

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
template_id = next(x for x in flair_choices if x['flair_text'].replace(':','') == sys.argv[1])['flair_template_id']
submission.flair.select(template_id)