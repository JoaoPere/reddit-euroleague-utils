from reddit_utils import prepare_dot_env
import praw
import os
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
import csv
from collections import Counter
import re
import sys


def printAllFlairsAssigned(subreddit):
    redditors_flairs = [re.sub(r":.*:\s", "", template['flair_text'])
                        for template in subreddit.flair(limit=None)]

    redditors_flairs_counter = Counter(redditors_flairs)
    all_elements = redditors_flairs_counter.most_common()

    print('Flair| Count')
    print('---|---')
    for flair_count in all_elements:
        print('{} | {}'.format(flair_count[0], flair_count[1]))

    print()
    print('Total number of teams with flairs assigned: {}'.format(
        len(redditors_flairs_counter)))
    print('Total flairs assigned: {}'.format(len(redditors_flairs)))


def printRedditorsFromClub(subreddit, club):
    redditors_flairs_club = [(re.sub(r":.*:\s", "", template['flair_text']), template['user'].name)
                             for template in subreddit.flair(limit=None)]

    club_fans = list(filter(lambda f: f[0] == club, redditors_flairs_club))
    redditor_names = list(map(lambda f: 'u/{}'.format(f[1]), club_fans))

    print(', '.join(redditor_names))


if __name__ == "__main__":
    flairs_dict = dict()

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Post Game Thread Generator Script")

    subreddit = reddit.subreddit("Euroleague")

    printAllFlairsAssigned(subreddit)
    # printRedditorsFromClub(subreddit, 'Žalgiris Kaunas')
