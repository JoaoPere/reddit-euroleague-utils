from selenium import webdriver
from threading import Timer
from bs4 import BeautifulSoup
from enum import Enum
import sys
import signal
import os
from functools import partial
from collections import namedtuple

# TODO: Improve imports, perhaps circunstancial function declarations changes
from postgame import REDDIT_THREAD_PLACEHOLDER_TEXT, createEmptyThread, updateThread, getTodaysPostGameThreads, getGamesLinks


class ThreadState(Enum):
    UNPUBLISHED = 0,
    PUBLISHING = 1
    PUBLISHED = 2,
    COMPLETED = 3


class GameState(Enum):
    UNFINISHED = 0,
    FINISHED = 1


LOOP_TIME = 120


class RedditGameThread():
    def __init__(self, home_team, away_team, competition, comp_round=None, comp_stage=None, game_state=GameState.UNFINISHED, thread_state=ThreadState.UNPUBLISHED, game_link=None, reddit_submission=None):
        self.home_team = home_team
        self.away_team = away_team
        self.competition = competition

        self.comp_round = comp_round
        self.comp_stage = comp_stage

        self.game_state = game_state
        self.thread_state = thread_state

        self.game_link = game_link
        self.reddit_submission = reddit_submission

    def __str__(self):
        return "{} vs {} in {} - {} / {}\nGame Link: {}\nReddit Submission: {}\n".format(self.home_team, self.away_team, self.competition, self.game_state, self.thread_state, self.game_link, self.reddit_submission)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, RedditGameThread):
            return self.home_team == other.home_team and self.away_team == other.away_team and self.competition == other.competition
        return False

    @property
    def home_team(self):
        return self._home_team

    @home_team.setter
    def home_team(self, value):
        self._home_team = value

    @property
    def away_team(self):
        return self._away_team

    @away_team.setter
    def away_team(self, value):
        self._away_team = value

    @property
    def competition(self):
        return self._competition

    @competition.setter
    def competition(self, value):
        self._competition = value

    @property
    def comp_round(self):
        return self._comp_round

    @comp_round.setter
    def comp_round(self, value):
        self._comp_round = value

    @property
    def comp_stage(self):
        return self._comp_stage

    @comp_stage.setter
    def comp_stage(self, value):
        self._comp_stage = value

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        if value not in GameState:
            raise ValueError('Invalid game state')

        self._game_state = value

    @property
    def thread_state(self):
        return self._thread_state

    @thread_state.setter
    def thread_state(self, value):
        if value not in ThreadState:
            raise ValueError('Invalid thread state')

        self._thread_state = value

    @property
    def game_link(self):
        return self._game_link

    @game_link.setter
    def game_link(self, value):
        self._game_link = value

    @property
    def reddit_submission(self):
        return self._reddit_submission

    @reddit_submission.setter
    def reddit_submission(self, value):
        self._reddit_submission = value

    # Improve error handling
    def publishThread(self, args_info):
        self.thread_state = ThreadState.PUBLISHING

        self.reddit_submission = createEmptyThread(
            self.home_team, self.away_team, self.comp_round, self.comp_stage, self.args_info)

        if self.reddit_submission is not None:
            self.thread_state = ThreadState.PUBLISHED

    # Improve error handling
    def updateThread(self):
        if self.reddit_submission is None:
            raise ValueError('Reddit Thread should not be null')

        self.reddit_submission, updated = updateThread(
            self.home_team, self.away_team, self.reddit_submission, self.game_link)

        if updated:
            self._thread_state = ThreadState.COMPLETED


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def updateTodaysGamesFlashScore(driver, games_list, args_info):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    live_table = soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all(
        'div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find(
            'div', class_='event__participant--home').text
        away_team = game_table.find(
            'div', class_='event__participant--away').text

        reddit_game_thread = RedditGameThread(
            home_team, away_team, args_info.comp_full_name)

        if reddit_game_thread not in games_list:
            games_list.append(reddit_game_thread)

    return games_list


def updateThreads(games_list, args_info):
    num_games_completed = 0

    for game_reddit in games_list:
        print(game_reddit)
        if game_reddit.game_state == GameState.FINISHED:
            if game_reddit.thread_state == ThreadState.UNPUBLISHED:
                game_reddit.publishThread(args_info)
            elif game_reddit.thread_state == ThreadState.PUBLISHED:
                game_reddit.updateThread()
            elif game_reddit.thread_state == ThreadState.COMPLETED:
                num_games_completed += 1

    if num_games_completed == len(games_list):
        os.kill(os.getpid(), signal.SIGUSR1)  # pylint: disable=E1101

# TODO: Improve checking conditions for finished games. Possible try/catch blocks


def loop(games_list, args_info):
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
            home_team, away_team, args_info.comp_full_name, game_state=game_state)

        index = games_list.index(reddit_game_thread)
        if index is not None:
            games_list[index].game_state = game_state

    updateThreads(games_list, args_info)


def service_shutdown(driver, timer, *args):
    print("Shutting down the service")
    timer.stop()
    driver.quit()


def populateExistingPostMatchThreads(args_info):
    games_list = list()
    post_game_threads = getTodaysPostGameThreads(args_info.comp_full_name)

    for game_thread in post_game_threads:
        submission = game_thread[0]

        thread_state = ThreadState.PUBLISHED if submission.selftext == REDDIT_THREAD_PLACEHOLDER_TEXT else ThreadState.COMPLETED

        home_team, away_team = game_thread[1]

        reddit_game_thread = RedditGameThread(home_team, away_team, args_info.comp_full_name,
                                              thread_state=thread_state, game_state=GameState.FINISHED, reddit_submission=submission)
        games_list.append(reddit_game_thread)

    return games_list


def printUsage():
    pass


if __name__ == '__main__':
    ArgsParseTuple = namedtuple(
        'ArgsParseTuple', 'fs_link comp_results_link comp_home_link comp_full_name comp_small_name')
    args_dict = dict()

    args_dict['EL'] = ArgsParseTuple('https://www.flashscore.com/basketball/europe/euroleague/',
                                     'https://www.euroleague.net/main/results', 'https://www.euroleague.net', 'EuroLeague', 'EL')
    args_dict['EC'] = ArgsParseTuple('https://www.flashscore.com/basketball/europe/eurocup/',
                                     'https://www.eurocupbasketball.com/eurocup/games/results', 'https://www.eurocupbasketball.com', 'EuroCup', 'EC')

    if(sys.argv[1] not in args_dict):
        printUsage()
        sys.exit()

    RedditGameThread.args_info = args_dict.get(sys.argv[1])

    driver = webdriver.Firefox()
    driver.get(RedditGameThread.args_info.fs_link)

    games_list = populateExistingPostMatchThreads(RedditGameThread.args_info)
    print('Populated {} games from Reddit'.format(len(games_list)))
    games_list = updateTodaysGamesFlashScore(
        driver, games_list, RedditGameThread.args_info)
    print('FlashScore added the total ammount of today\'s games to {}\n'.format(
        len(games_list)))
    games_list = getGamesLinks(games_list, RedditGameThread.args_info)

    # it auto-starts, no need of rt.start()
    rt = RepeatedTimer(LOOP_TIME, loop, games_list, RedditGameThread.args_info)
    signal.signal(signal.SIGUSR1, partial(  # pylint: disable=E1101
        service_shutdown, driver, rt))
