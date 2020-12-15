from utils.repeatedtimer import RepeatedTimer
from utils.redditgamethread import RedditGameThread
from utils.enumstates import ThreadState, GameState
from utils.prepare import populate_existing_postmatch_threads, add_flashscore_games, fill_game_details
from reddit_utils.subreddit import get_subreddit
from selenium import webdriver
from collections import namedtuple
from functools import partial
from bs4 import BeautifulSoup
import sys
import signal
import os
import re
import argparse


def handle_thread_updates(games_list):
    num_games_completed = 0

    for game_reddit in games_list:
        print()
        print(game_reddit)
        if game_reddit.game_state == GameState.FINISHED:
            if game_reddit.thread_state == ThreadState.UNPUBLISHED:
                game_reddit.publish_thread()
            elif game_reddit.thread_state == ThreadState.PUBLISHED:
                game_reddit.update_thread()
            elif game_reddit.thread_state == ThreadState.COMPLETED:
                num_games_completed += 1

    print()
    print('------------------------')

    if num_games_completed == len(games_list):
        os.kill(os.getpid(), signal.SIGUSR1)  # pylint: disable=E1101


def loop(driver, games_list):
    updated_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Finds Today's Matches games table
    live_table = updated_soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all(
        'div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find(
            'div', class_='event__participant--home').text
        away_team = game_table.find(
            'div', class_='event__participant--away').text

        # Markup is different for games yet to start. Skip loop step if that is the case
        if game_table.find('div', class_='event__time'):
            continue

        game_state = game_table.find('div', class_='event__stage--block').text

        # Parse FlashScore states to match the application states
        game_state = GameState.FINISHED if game_state == 'Finished' or game_state == 'After Overtime' else GameState.UNFINISHED

        reddit_game_thread = RedditGameThread(
            home_team, away_team, game_state=game_state)

        index = games_list.index(reddit_game_thread)
        if index is not None:
            games_list[index].game_state = game_state

    handle_thread_updates(games_list)


def service_shutdown(driver, timer, *args):
    print("Shutting down the service")
    timer.stop()
    driver.quit()


def printUsage():
    pass


def get_games_list(driver):
    games_list = populate_existing_postmatch_threads()
    print('Populated {} games from Reddit'.format(len(games_list)))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    games_list = add_flashscore_games(
        soup, games_list)

    print('FlashScore added the total ammount of today\'s games to {}\n'.format(
        len(games_list)))

    fill_game_details(games_list)

    return games_list


def get_competition_info(competition):
    ArgsParseTuple = namedtuple(
        'ArgsParseTuple', 'fs_link comp_results_link comp_home_link comp_full_name comp_small_name')
    args_dict = dict()

    args_dict['EL'] = ArgsParseTuple('https://www.flashscore.com/basketball/europe/euroleague/',
                                     'https://www.euroleague.net/main/results', 'https://www.euroleague.net', 'EuroLeague', 'EL')
    args_dict['EC'] = ArgsParseTuple('https://www.flashscore.com/basketball/europe/eurocup/',
                                     'https://www.eurocupbasketball.com/eurocup/games/results', 'https://www.eurocupbasketball.com', 'EuroCup', 'EC')

    return args_dict.get(competition)


def main():
    parser = argparse.ArgumentParser(
        description='Post game thread bot creator')
    parser.add_argument('competition', metavar='C',
                        type=str, choices=['EL', 'EC'])
    parser.add_argument('loop', metavar='L', type=int)
    args = parser.parse_args()
    comp_info = get_competition_info(args.competition)

    RedditGameThread.set_competition_info(comp_info)

    driver = webdriver.Firefox()
    driver.get(comp_info.fslink)

    games_list = get_games_list(driver)

    # it auto-starts, no need of rt.start()
    rt = RepeatedTimer(args.loop, loop, driver, games_list)
    signal.signal(signal.SIGUSR1, partial(  # pylint: disable=E1101
        service_shutdown, driver, rt))


if __name__ == '__main__':
    main()
