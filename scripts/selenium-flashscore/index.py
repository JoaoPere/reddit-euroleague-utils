from selenium import webdriver
from threading import Timer
from time import sleep
from pprint import pprint
from bs4 import BeautifulSoup
import subprocess
from enum import Enum
import sys
import signal
import os
from functools import partial

class ThreadState(Enum):
	UNPUBLISHED = 0,
	PUBLISHED = 1,
	COMPLETED = 2

class GameState(Enum):
	UNFINISHED = 0,
	FINISHED = 1

class RedditGameThread():
	def __init__(self, home_team, away_team, game_state=GameState.UNFINISHED):
		self._home_team = home_team
		self._away_team = away_team
		self._game_state = game_state
		self._thread_state = ThreadState.UNPUBLISHED

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
		pass

	def updateThread(self):
		pass

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

driver = webdriver.Firefox()
#driver.get('https://www.flashscore.com/basketball/europe/euroleague/')
driver.get('https://www.flashscore.com/basketball/asia/abl/')

def getTodaysGames(driver):
	soup = BeautifulSoup(driver.page_source,'html.parser')
	todays_games = list()

	live_table = soup.find('div', class_='leagues--live')
	all_live_games_table = live_table.find_all('div', {"class": "event__match"})

	for game_table in all_live_games_table:
		home_team = game_table.find('div', class_='event__participant--home').text
		away_team = game_table.find('div', class_='event__participant--away').text

		reddit_game_thread = RedditGameThread(home_team, away_team)
		todays_games.append(reddit_game_thread)

	print('Today\'s games length: {}'.format(len(todays_games)))
	return todays_games

def updateThreads(games_list):
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
				print('Exiting')
				os.kill(os.getpid(), signal.SIGUSR1)
				
		elif game_reddit.game_state == GameState.UNFINISHED:
			print('Waiting for game to end')

def loop(games_list):
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

		reddit_game_thread = RedditGameThread(home_team, away_team, game_state)
		
		if reddit_game_thread in games_list:
			index = games_list.index(reddit_game_thread)
			games_list[index].game_state = game_state

			print('{} vs {} => {}'.format(home_team, away_team, game_state))

	updateThreads(games_list)

def service_shutdown(driver):
	print('SIGINT received')
	print(driver)
	driver.quit()
	sys.exit()

signal.signal(signal.SIGUSR1, partial(service_shutdown, driver))

games_list = getTodaysGames(driver)
rt = RepeatedTimer(5, loop, games_list) # it auto-starts, no need of rt.start()