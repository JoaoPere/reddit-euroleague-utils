from .enumstates import ThreadState, GameState
from .redditgamethread import RedditGameThread
from reddit_utils.team_structs import team_info_by_fs
from reddit_utils.constants import REDDIT_THREAD_PLACEHOLDER_TEXT
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta
import requests
import urllib.parse
import re
import sys

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=sys.maxsize))
s.mount('https://', HTTPAdapter(max_retries=sys.maxsize))


def extract_thread_title_information(thread_title):
    # Return home_team and away team in Reddit format
    title_group_regex = r"Post-Match Thread: (?P<home_team>.*?) - (?P<away_team>.*?) \[(?P<competition>(\w+))"
    title_group = re.search(title_group_regex, thread_title)

    home_team = find_flashscore_name_by_reddit_name(
        title_group.group('home_team').strip())
    away_team = find_flashscore_name_by_reddit_name(
        title_group.group('away_team').strip())

    return home_team, away_team


def find_flashscore_name_by_reddit_name(name):
    for fsname in team_info_by_fs.keys():
        other_names = team_info_by_fs[fsname]

        if other_names.reddit == name:
            return fsname

    return None


def get_todays_threads():
    now = datetime.utcnow()  # - timedelta(days=30)
    threads = list()

    new_submissions = RedditGameThread.subreddit.new(limit=100)

    for submission in new_submissions:
        timestamp = submission.created_utc
        time = datetime.fromtimestamp(timestamp)

        # Figure out why it is not possible to break the loop inside the ternary operator
        if time.date() == now.date():
            threads.append(submission)
        else:
            break

    return threads


def populate_existing_postmatch_threads():
    games_list = list()
    post_game_threads = get_todays_postgame_threads()

    for game_thread in post_game_threads:
        submission = game_thread[0]

        thread_state = ThreadState.PUBLISHED if submission.selftext == REDDIT_THREAD_PLACEHOLDER_TEXT else ThreadState.COMPLETED

        home_team, away_team = game_thread[1]

        reddit_game_thread = RedditGameThread(home_team, away_team,
                                              thread_state=thread_state, game_state=GameState.FINISHED, reddit_submission=submission)
        games_list.append(reddit_game_thread)

    return games_list


def get_todays_postgame_threads():
    todays_threads = get_todays_threads()

    title_regex = r"Post-Match Thread: (.*?)-(.*?)\[" + \
        re.escape(RedditGameThread.comp_info.comp_full_name) + r"(.*?)\]"
    post_game_threads = [(thread, extract_thread_title_information(thread.title))
                         for thread in todays_threads if re.match(title_regex, thread.title)]

    return post_game_threads


def add_flashscore_games(soup, games_list):
    live_table = soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all(
        'div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find(
            'div', class_='event__participant--home').text
        away_team = game_table.find(
            'div', class_='event__participant--away').text

        game_state = game_table.find('div', class_='event__stage--block')
        game_is_postponed = False

        if game_state is not None:
            game_state = game_state.text
            game_is_postponed = True if game_state == 'Postponed' else False

        if not game_is_postponed:
            reddit_game_thread = RedditGameThread(
                home_team, away_team, RedditGameThread.comp_info.comp_full_name)

            if reddit_game_thread not in games_list:
                games_list.append(reddit_game_thread)

    return games_list


def fill_game_details(games_list, game_number=None):
    if game_number is None:
        r = requests.get(RedditGameThread.comp_info.comp_results_link)
    else:
        url_args_dict = dict()
        url_args_dict['gamenumber'] = game_number
        params = urllib.parse.urlencode(url_args_dict, doseq=True)
        r = requests.get('{}?{}'.format(
            RedditGameThread.comp_info.comp_results_link, params))

    soup = BeautifulSoup(r.text, 'html.parser')

    stage_round_spans = soup.find('div', class_='gc-title').find_all('span')
    comp_stage = stage_round_spans[1].text
    comp_round = stage_round_spans[2].text

    all_games_div = soup.find('div', class_='wp-module-asidegames')
    all_game_links = all_games_div.find_all('a', class_='game-link')

    has_none_game_link = False

    for game in games_list:
        if game.game_link is None:
            game_link = get_game_link(
                game.home_team, game.away_team, all_game_links)

            if game_link is None:
                has_none_game_link = True
            else:
                game.game_link = game_link
                game.comp_round = comp_round
                game.comp_stage = comp_stage

    if has_none_game_link:
        # Assumes postponments only
        round_int = int(comp_round.replace("Round ", ""))
        round_int -= 1
        fill_game_details(games_list, round_int)
    else:
        return games_list


def get_game_link(home_team, away_team, all_game_links):
    home_team_parsed = team_info_by_fs.get(home_team)
    away_team_parsed = team_info_by_fs.get(away_team)

    for a_game in all_game_links:
        clubs = a_game.find_all('div', class_='club')

        home_club_name = clubs[0].find('span', class_='name').text
        away_club_name = clubs[1].find('span', class_='name').text

        if home_team_parsed.official == home_club_name and away_team_parsed.official == away_club_name:
            game_link = RedditGameThread.comp_info.comp_home_link + \
                a_game['href']

            return game_link

    return None
