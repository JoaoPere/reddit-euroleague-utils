from reddit_utils import prepare_dot_env
from reddit_utils.subreddit import get_subreddit
from standings import get_standings_table
from schedule import get_schedule_table
from results import get_results_table
import sys
import praw
import re
import os
import argparse


def update_old_reddit(subreddit, sidebar_tables):
    results_table_old_urls = re.sub(
        'https://www.reddit.com/', 'http://old.reddit.com/', sidebar_tables['Results'])

    with open('old_sidebar_boilerplate.txt', mode='r') as bp:
        bp_content = bp.read()
        sidebar_text = bp_content.format(
            standings=sidebar_tables['Standings'], results=results_table_old_urls, schedule=sidebar_tables['Schedule'])
        subreddit.mod.update(description=sidebar_text)

    print('Successfully updated Old Reddit sidebar description')


def update_new_reddit(subreddit, sidebar_tables):
    widgets = subreddit.widgets
    widgets.progressive_images = True

    for widget in widgets.sidebar[:-1]:
        widget_name = widget.shortName

        table = sidebar_tables.get(widget_name)

        if table:
            widget.mod.update(text=table)
            print('Successfully updated widget: {}'.format(widget_name))


def main():
    parser = argparse.ArgumentParser(description="Sidebar update")
    parser.add_argument('week', metavar='W', type=int)
    args = parser.parse_args()

    standings_table = get_standings_table()
    results_table = get_results_table(args.week)
    schedule_table = get_schedule_table(args.week + 1)

    subreddit = get_subreddit()

    sidebar_tables = dict()
    sidebar_tables['Standings'] = standings_table
    sidebar_tables['Results'] = results_table
    sidebar_tables['Schedule'] = schedule_table

    update_new_reddit(subreddit, sidebar_tables)
    update_old_reddit(subreddit, sidebar_tables)


if __name__ == '__main__':
    main()
