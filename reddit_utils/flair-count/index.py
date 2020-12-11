from reddit_utils import prepare_dot_env
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
from collections import Counter
import csv
import re
import sys
import argparse
import praw
import os


def get_flair_table_list(subreddit):
    redditors_flairs = [re.sub(r":.*:\s", "", template['flair_text'])
                        for template in subreddit.flair(limit=None)]

    redditors_flairs_counter = Counter(redditors_flairs)
    all_elements = redditors_flairs_counter.most_common()

    flair_table_list = list()

    flair_table_list.append('Flair| Count')
    flair_table_list.append('---|---')
    for flair_count in all_elements:
        flair_table_list.append('{} | {}'.format(
            flair_count[0], flair_count[1]))

    flair_table_list.append('')
    flair_table_list.append('Total number of teams with flairs assigned: {}'.format(
        len(redditors_flairs_counter)))
    flair_table_list.append(
        'Total flairs assigned: {}'.format(len(redditors_flairs)))
    return flair_table_list


def print_redditors_from_club(subreddit, club):
    redditors_flairs_club = [(re.sub(r":.*:\s", "", template['flair_text']), template['user'].name)
                             for template in subreddit.flair(limit=None)]

    club_fans = list(filter(lambda f: f[0] == club, redditors_flairs_club))
    redditor_names = list(map(lambda f: 'u/{}'.format(f[1]), club_fans))

    print(', '.join(redditor_names))


def save_flair_count(flair_table_list, year, month):
    count_filename = "{}_{}.txt".format(year, month)
    counts_filepath = os.path.join(
        os.getcwd(), '..', 'flair-breakdown', 'counts', count_filename)
    with open(counts_filepath, mode='w', encoding='utf8') as f:
        f.writelines("%s\n" % line for line in flair_table_list[:-1])
        f.write("%s" % flair_table_list[-1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flair counter")
    parser.add_argument('--team', '-t', dest='team',
                        type=str, nargs=1, metavar='t')
    parser.add_argument('--save, -s', dest='save', type=int, nargs=2)
    args = parser.parse_args()

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Post Game Thread Generator Script")

    subreddit = reddit.subreddit("Euroleague")

    try:
        team_name = args.team[0]
        print_redditors_from_club(subreddit, team_name)
    except:
        flair_table_list = get_flair_table_list(subreddit)
        print('\n'.join(flair_table_list))
        if args.save:
            year = str(args.save[0])
            month = str(args.save[1])

            save_flair_count(flair_table_list[:-3], year, month)
