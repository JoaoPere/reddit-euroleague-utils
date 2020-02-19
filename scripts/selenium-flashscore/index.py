from selenium import webdriver
from threading import Timer
from bs4 import BeautifulSoup
from enum import Enum
import sys
import signal
import os
from functools import partial

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
            return self.home_team == other.home_team and self.away_team == other.away_team
        return False

    @property
    def home_team(self):
        return self._home_team
    
    @property
    def away_team(self):
        return self._away_team
    
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

    def publishThread(self):
        self._reddit_submission, self._game_link = createEmptyThread(self.home_team, self.away_team, self.competition)
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


def updateTodaysGamesFlashScore(driver, games_list, comp):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    todays_games = list()

    live_table = soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all('div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find('div', class_='event__participant--home').text
        away_team = game_table.find('div', class_='event__participant--away').text

        reddit_game_thread = RedditGameThread(home_team, away_team, comp)
        
        if reddit_game_thread not in games_list:
            todays_games.append(reddit_game_thread)
            
    return todays_games

def updateThreads(games_list):
    num_games_completed = 0
    for game_reddit in games_list:
        if game_reddit.game_state == GameState.FINISHED:
            if game_reddit.thread_state == ThreadState.UNPUBLISHED:
                print('Publishing Thread')
                game_reddit.publishThread()
                game_reddit.thread_state = ThreadState.PUBLISHED
            elif game_reddit.thread_state == ThreadState.PUBLISHED:
                print('Updating Thread')
                game_reddit.updateThread()
                game_reddit.thread_state = ThreadState.COMPLETED
            elif game_reddit.thread_state == ThreadState.COMPLETED:
                print('Game Thread complete')
                num_games_completed += 1
                
        elif game_reddit.game_state == GameState.UNFINISHED:
            print('Waiting for game to end')
    
    if num_games_completed == len(games_list):
        os.kill(os.getpid(), signal.SIGUSR1)

def loop(games_list, comp):
    updated_soup = BeautifulSoup(driver.page_source,'html.parser')
    
    # Finds Today's Matches games table
    live_table = updated_soup.find('div', class_='leagues--live')
    all_live_games_table = live_table.find_all('div', {"class": "event__match"})

    for game_table in all_live_games_table:
        home_team = game_table.find('div', class_='event__participant--home').text
        away_team = game_table.find('div', class_='event__participant--away').text
        game_state = game_table.find('div', class_='event__stage--block').text

        # Parse FlashScore states to match the application states
        game_state = GameState.FINISHED if game_state == 'Finished' else GameState.UNFINISHED

        reddit_game_thread = RedditGameThread(home_team, away_team, comp, game_state=game_state)
        
        if reddit_game_thread in games_list:
            index = games_list.index(reddit_game_thread)
            games_list[index].game_state = game_state

            print('{} vs {} => {}'.format(home_team, away_team, comp, game_state))

    updateThreads(games_list)

def service_shutdown(driver, timer, *args):
    print("Shutting down the service")
    timer.stop()
    driver.quit()
    
def populateExistingPostMatchThreads(comp):    
    games_list = list()
    post_game_threads = getTodaysPostGameThreads(comp)
    for game_thread in post_game_threads:
        submission = game_thread[0]
        
        thread_state = ThreadState.PUBLISHED if submission.selftext == REDDIT_THREAD_PLACEHOLDER_TEXT else ThreadState.COMPLETED
        
        home_team, away_team = game_thread[1]
   
        reddit_game_thread = RedditGameThread(home_team, away_team, comp, thread_state = thread_state , game_state = GameState.FINISHED, reddit_submission = submission)
        games_list.append(reddit_game_thread)
        
    return games_list
    
if __name__ == '__main__':
    url = str()
    if sys.argv[1] == 'EL':
        url = 'https://www.flashscore.com/basketball/europe/euroleague/'
    elif sys.argv[1] == 'EC':
        url = 'https://www.flashscore.com/basketball/europe/eurocup/'
    
    driver = webdriver.Firefox()
    #driver.get(url)
    driver.get(url)
    
    games_list = populateExistingPostMatchThreads(sys.argv[1])
    print('Populated {} games from Reddit'.format(len(games_list)))
    games_list = updateTodaysGamesFlashScore(driver, games_list, sys.argv[1])
    print('FlashScore added the total ammount of today\'s games to {}'.format(len(games_list)))
    
    rt = RepeatedTimer(30, loop, games_list, sys.argv[1]) # it auto-starts, no need of rt.start()
    signal.signal(signal.SIGUSR1, partial(service_shutdown, driver, rt))