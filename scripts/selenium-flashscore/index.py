from selenium import webdriver
from threading import Timer
from bs4 import BeautifulSoup
from enum import Enum
import sys
import signal
import os
from functools import partial
from collections import namedtuple

from postgame import createEmptyThread, updateThread, getTodaysPostGameThreads, REDDIT_THREAD_PLACEHOLDER_TEXT

class ThreadState(Enum):
    UNPUBLISHED = 0,
    PUBLISHED = 1,
    COMPLETED = 2

class GameState(Enum):
    UNFINISHED = 0,
    FINISHED = 1
    

class RedditGameThread():
    def __init__(self, home_team, away_team, competition, game_state=GameState.UNFINISHED, thread_state=ThreadState.UNPUBLISHED, game_link=None, reddit_submission=None):
        self._home_team = home_team
        self._away_team = away_team
        self._competition = competition
        
        self._game_state = game_state
        self._thread_state = thread_state
        
        self._game_link = game_link
        self._reddit_submission = reddit_submission

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, RedditGameThread):
            return self.home_team == other.home_team and self.away_team == other.away_team and self.competition == other.competition
        return False

    @property
    def home_team(self):
        return self._home_team
    
    @property
    def away_team(self):
        return self._away_team
    
    @property
    def competition(self):
        return self._competition
    
    @property
    def thread_state(self):
        return self._thread_state

    @thread_state.setter
    def thread_state(self, value):
        if value not in ThreadState:
            raise ValueError('Invalid thread state')

        self._thread_state = value

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        if value not in GameState:
            raise ValueError('Invalid game state')

        self._game_state = value

    def publishThread(self, args_info):
        self._reddit_submission, self._game_link = createEmptyThread(self.home_team, self.away_team, args_info)
        self._thread_state = ThreadState.PUBLISHED
        
    def updateThread(self):
        if self._reddit_submission is None:
            raise ValueError('Reddit Thread should not be null')
            
        self._reddit_submission, updated = updateThread(self._home_team, self._away_team, self._reddit_submission, self._game_link)
        if updated:
            self._thread_state = ThreadState.COMPLETED

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
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
    soup = BeautifulSoup(driver.page_source,'html.parser')
    todays_games = list()

    live_table = soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all('div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find('div', class_='event__participant--home').text
        away_team = game_table.find('div', class_='event__participant--away').text

        reddit_game_thread = RedditGameThread(home_team, away_team, args_info.comp_full_name)
        
        if reddit_game_thread not in games_list:
            todays_games.append(reddit_game_thread)
            
    return todays_games

def updateThreads(games_list, args_info):
    num_games_completed = 0
    
    print('---------------------------------')

    for game_reddit in games_list:
        print('{} vs {} => {} - {}'.format(game_reddit.home_team, game_reddit.away_team, game_reddit.game_state, game_reddit.thread_state))
        if game_reddit.game_state == GameState.FINISHED:
            if game_reddit.thread_state == ThreadState.UNPUBLISHED:
                print('Publishing thread')
                game_reddit.publishThread(args_info)
            elif game_reddit.thread_state == ThreadState.PUBLISHED:
                print('Trying to update thread')
                game_reddit.updateThread()
            elif game_reddit.thread_state == ThreadState.COMPLETED:
                print('Post-Match thread complete')
                num_games_completed += 1
                
        elif game_reddit.game_state == GameState.UNFINISHED:
               print('Game is yet to end')
                              
    if num_games_completed == len(games_list):
        os.kill(os.getpid(), signal.SIGUSR1)

#TODO: Improve checking conditions for finished games. Possible try/catch blocks
def loop(games_list, args_info):
    updated_soup = BeautifulSoup(driver.page_source,'html.parser')
    
    # Finds Today's Matches games table
    live_table = updated_soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all('div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find('div', class_='event__participant--home').text
        away_team = game_table.find('div', class_='event__participant--away').text
        
        # Markup is different for games yet to start. Skip loop step if that is the case
        if game_table.find('div', class_='event__time'):
            continue
            
        game_state = game_table.find('div', class_='event__stage--block').text

        # Parse FlashScore states to match the application states
        game_state = GameState.FINISHED if game_state == 'Finished' else GameState.UNFINISHED

        reddit_game_thread = RedditGameThread(home_team, away_team, args_info.comp_full_name, game_state=game_state)
        
        if reddit_game_thread in games_list:
            index = games_list.index(reddit_game_thread)
            games_list[index].game_state = game_state
            
    updateThreads(games_list, args_info)

def service_shutdown(driver, timer, *args):
    print("Shutting down the service")
    timer.stop()
    driver.quit()
    
def populateExistingPostMatchThreads(args_info):    
    games_list = list()
    post_game_threads = getTodaysPostGameThreads(args_info)
    
    for game_thread in post_game_threads:
        submission = game_thread[0]
        
        thread_state = ThreadState.PUBLISHED if submission.selftext == REDDIT_THREAD_PLACEHOLDER_TEXT else ThreadState.COMPLETED
        
        home_team, away_team = game_thread[1]
   
        reddit_game_thread = RedditGameThread(home_team, away_team, args_info.comp_full_name, thread_state = thread_state , game_state = GameState.FINISHED, reddit_submission = submission)
        games_list.append(reddit_game_thread)
        
    return games_list

def printUsage():
    pass
    
if __name__ == '__main__':
    ArgsParseTuple = namedtuple('ArgsParseTuple', 'fslink comp_results_link comp_home_link comp_full_name comp_small_name')
    args_dict = dict()
    
    args_dict['EL'] = ArgsParseTuple('https://www.flashscore.com/basketball/europe/euroleague/', 'https://www.euroleague.net/main/results', 'https://www.euroleague.net', 'EuroLeague', 'EL')
    args_dict['EC'] = ArgsParseTuple('https://www.flashscore.com/basketball/europe/eurocup/', 'https://www.eurocupbasketball.com/eurocup/games/results', 'https://www.eurocupbasketball.com', 'EuroCup', 'EC')
    
    if(sys.argv[1] not in args_dict):
        printUsage()
        sys.exit()
    
    args_info = args_dict.get(sys.argv[1])
    
    driver = webdriver.Firefox()
    #driver.get(url)
    driver.get(args_info.fslink)
    
    games_list = populateExistingPostMatchThreads(args_info)
    print('Populated {} games from Reddit'.format(len(games_list)))
    games_list = updateTodaysGamesFlashScore(driver, games_list, args_info)
    print('FlashScore added the total ammount of today\'s games to {}'.format(len(games_list)))
    
    rt = RepeatedTimer(30, loop, games_list, args_info) # it auto-starts, no need of rt.start()
    signal.signal(signal.SIGUSR1, partial(service_shutdown, driver, rt))