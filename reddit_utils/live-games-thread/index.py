from reddit_utils import prepare_dot_env
from reddit_utils.team_structs import team_info_by_official
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import praw
from collections import namedtuple
import os


team_names_parsed = dict()

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
                game_clubs = game.find_all('div', class_='club')

                game_home_team = team_info_by_official.get(
                    game_clubs[0].find('span', class_='name').text).reddit
                game_away_team = team_info_by_official.get(
                    game_clubs[1].find('span', class_='name').text).reddit

                game_md = "{home_team} - {away_team} | {hours}:{minutes} CET  | {group_name}".format(home_team=bold(game_home_team), away_team=bold(
                    game_away_team), hours=game_date.strftime('%H'), minutes=game_date.strftime('%M'), group_name=group_name)

                games_markdown.append((game_date, game_md))

        games_markdown.sort(key=lambda d: d[0])

    return games_markdown


def getEuroLeagueGames(now_time, soup):
    all_games = soup.find_all('div', class_='livescore')[
        1].find_all('div', class_='game')

    games_markdown = list()

    for game in all_games:
        game_date = game.find('span', class_='date').text

        game_date = game_date.strip()[:len(game_date) - 4]
        game_date = datetime.strptime(game_date, "%B %d %H:%M")

        # Date is not set, continue to next game
        if game_date is None:
            continue

        if game_date.day == now_time.day and game_date.month == now_time.month:
            game_clubs = game.find_all('div', class_='club')

            game_home_team = team_info_by_official.get(
                game_clubs[0].find('span', class_='name').text).reddit
            game_away_team = team_info_by_official.get(
                game_clubs[1].find('span', class_='name').text).reddit

            game_md = "{home_team} - {away_team} | {hours}:{minutes} CET".format(home_team=bold(
                game_home_team), away_team=bold(game_away_team), hours=game_date.strftime('%H'), minutes=game_date.strftime('%M'))
            games_markdown.append((game_date, game_md))

    return games_markdown


def bold(text):
    return '**' + text + '**'


if __name__ == '__main__':
    ArgsParseTuple = namedtuple(
        'ArgsParseTuple', 'results_url comp_full_name comp_small_name markdown_function')
    args_dict = dict()

    args_dict['EL'] = ArgsParseTuple(
        'https://www.euroleague.net/main/results', 'EuroLeague', 'EL', getEuroLeagueGames)
    args_dict['EC'] = ArgsParseTuple(
        'https://www.eurocupbasketball.com/eurocup/games/results', 'EuroCup', 'EC', getEuroCupGames)

    if(sys.argv[1] not in args_dict):
        sys.exit()

    args_info = args_dict.get(sys.argv[1])

    now_time = datetime.now()
    r = requests.get(args_info.results_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    games_markdown = args_info.markdown_function(now_time, soup)

    if len(games_markdown) < 1:
        print("No games today in {}".format(args_info.comp_full_name))
        sys.exit()
    final_markdown = DOUBLE_NEWLINE.join(
        [*(list(zip(*games_markdown))[1]),  'Asking for or sharing illegal streams is NOT allowed!'])
    final_title = "{today_date} {competition} Matches Live Thread".format(
        today_date=now_time.strftime('%d %B %Y'), competition=args_info.comp_full_name)

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Live Game Thread Generator Script")

    el_sub = reddit.subreddit('Euroleague')

    submission = el_sub.submit(title=final_title, selftext=final_markdown)
    submission.mod.sticky()
    submission.mod.suggested_sort('new')

    flair_choices = submission.flair.choices()
    template_id = next(x for x in flair_choices if x['flair_text'].replace(
        ':', '') == args_info.comp_small_name)['flair_template_id']
    submission.flair.select(template_id)
