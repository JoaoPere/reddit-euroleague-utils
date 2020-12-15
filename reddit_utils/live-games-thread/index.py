from reddit_utils import prepare_dot_env
from reddit_utils.team_structs import team_info_by_official
import reddit_utils.helpers as rh
import reddit_utils.subreddit as sr
from datetime import datetime
from bs4 import BeautifulSoup
from collections import namedtuple
import urllib.parse
import requests
import sys
import praw
import os
import argparse


def get_eurocup_games(now_time, soup):
    group_container = soup.find_all('div', class_='group-container')
    games_markdown = list()

    for group in group_container:
        group_name = group.find('div', class_='group').text

        group_games = group.find_all('div', class_='game')

        for game in group_games:
            has_date = game.find('span', class_='date')

            if not has_date:
                continue

            game_date = has_date.text

            game_date = game_date.strip()[:len(game_date) - 4]
            game_date = datetime.strptime(game_date, "%B %d %H:%M")

            if game_date.day == now_time.day and game_date.month == now_time.month:
                game_clubs = game.find_all('div', class_='club')

                game_home_team = team_info_by_official.get(
                    game_clubs[0].find('span', class_='name').text).reddit
                game_away_team = team_info_by_official.get(
                    game_clubs[1].find('span', class_='name').text).reddit

                game_md = "{home_team} - {away_team} | {hours}:{minutes} CET | {group_name}".format(home_team=rh.bold(game_home_team), away_team=rh.bold(
                    game_away_team), hours=game_date.strftime('%H'), minutes=game_date.strftime('%M'), group_name=group_name)

                games_markdown.append((game_date, game_md))

    return games_markdown


def get_euroleague_games(now_time, soup):
    all_games = soup.find_all('div', class_='livescore')[
        1].find_all('div', class_='game')

    games_markdown = list()

    for game in all_games:
        has_date = game.find('span', class_='date')

        if not has_date:
            continue

        game_date = has_date.text

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

            game_md = "{home_team} - {away_team} | {hours}:{minutes} CET".format(home_team=rh.bold(
                game_home_team), away_team=rh.bold(game_away_team), hours=game_date.strftime('%H'), minutes=game_date.strftime('%M'))
            games_markdown.append((game_date, game_md))

    return games_markdown


def get_games_markdown_list(args_info, now_time, games_markdown=[], game_number=None):
    if game_number is None:
        r = requests.get(args_info.results_url)
    else:
        url_args_dict = dict()
        url_args_dict['gamenumber'] = game_number
        params = urllib.parse.urlencode(url_args_dict, doseq=True)
        r = requests.get('{}?{}'.format(args_info.results_url, params))

    soup = BeautifulSoup(r.text, 'html.parser')

    day_markdown = args_info.markdown_function(now_time, soup)
    games_markdown.extend(day_markdown)

    # Top-down approach: last round to be analysed is the 1st
    if game_number == 1:
        games_markdown.sort(key=lambda d: d[0])
        return games_markdown
    else:
        stage_round_spans = soup.find(
            'div', class_='gc-title').find_all('span')
        comp_round = stage_round_spans[2].text
        round_int = int(comp_round.replace("Round ", ""))
        round_int -= 1

        return get_games_markdown_list(args_info, now_time, games_markdown, round_int)


def get_competition_info(competition):
    ArgsParseTuple = namedtuple(
        'ArgsParseTuple', 'results_url comp_full_name comp_small_name markdown_function')
    args_dict = dict()

    args_dict['EL'] = ArgsParseTuple(
        'https://www.euroleague.net/main/results', 'EuroLeague', 'EL', get_euroleague_games)
    args_dict['EC'] = ArgsParseTuple(
        'https://www.eurocupbasketball.com/eurocup/games/results', 'EuroCup', 'EC', get_eurocup_games)

    return args_dict.get(sys.argv[1])


def build_thread_title_and_markdown(games_markdown_list, competition_info, now_time):
    if len(games_markdown_list) < 1:
        print("No games today in {}".format(
            competition_info.comp_full_name))
        sys.exit()
    final_markdown = rh.double_newline_join(
        [*(list(zip(*games_markdown_list))[1]),  'Asking for or sharing illegal streams is NOT allowed!'])
    final_title = "{today_date} {competition} Matches Live Thread".format(
        today_date=now_time.strftime('%d %B %Y'), competition=competition_info.comp_full_name)

    return final_title, final_markdown


def main():
    parser = argparse.ArgumentParser(description='Live thread creator')
    parser.add_argument('competition', metavar='C',
                        type=str, choices=['EL', 'EC'])

    args = parser.parse_args()
    competition_info = get_competition_info(args.competition)

    now_time = datetime.now()

    games_markdown_list = get_games_markdown_list(competition_info, now_time)
    title, markdown = build_thread_title_and_markdown(
        games_markdown_list, competition_info, now_time)

    subreddit = sr.get_subreddit()
    sr.submit_text_post(subreddit, title, markdown, sticky=True,
                        suggested_sort='new', flair_text=competition_info.comp_small_name)


if __name__ == '__main__':
    main()
