from standings import getStandingsTable
from schedule import getScheduleTable
from results import getResultsTable
import sys
import praw
import re

def updateOldReddit(subreddit, sidebar_tables):
	results_table_old_urls = re.sub('https://www.reddit.com/', 'https://old.reddit.com/', sidebar_tables['Results'])
	
	with open('old_sidebar_boilerplate.txt', mode='r') as bp:
		bp_content = bp.read()
		sidebar_text = bp_content.format(standings=sidebar_tables['Standings'], results=results_table_old_urls, schedule=sidebar_tables['Schedule'])
		subreddit.mod.update(description=sidebar_text)
		
	print('Successfully updated Old Reddit sidebar description')

def updateNewReddit(subreddit, sidebar_tables):
	widgets = subreddit.widgets
	widgets.progressive_images = True

	for widget in widgets.sidebar[:-1]:
		widget_name = widget.shortName

		table = sidebar_tables.get(widget_name)
		
		if table:
			widget.mod.update(text=table)
			print('Successfully updated widget: {}'.format(widget_name))
		
if __name__ == '__main__':
	gameweek_number = int(sys.argv[1])

	# TODO: Add support to playoffs
	standings_table = getStandingsTable()
	results_table = getResultsTable(gameweek_number)
	schedule_table = getScheduleTable(gameweek_number + 1)

	reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
	                     client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
	                     password='tQ#1O&4k32Xy',
	                     user_agent='Euroleague Post-Game Thread Script',
	                     username='Al-Farrekt-Aminu')
	
	el_sub = reddit.subreddit('Euroleague')
	
	sidebar_tables = dict()
	sidebar_tables['Standings'] = standings_table
	sidebar_tables['Results'] = results_table
	sidebar_tables['Schedule'] = schedule_table
	
	updateNewReddit(el_sub, sidebar_tables)
	updateOldReddit(el_sub, sidebar_tables)