from reddit_utils import prepare_dot_env
import praw
import os
import sqlite3


def getRedditorsYetToConvert(conn):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT redditor_name FROM user_flairs_dms WHERE has_converted=0")
    all_users = cursor.fetchall()

    return [user[0] for user in all_users]


def getRedditorsWithFlair(subreddit):
    return [template['user'].name
            for template in subreddit.flair(limit=None)]


def updateConvertedRedditors(redditors_with_flair, redditors_yet_to_convert, conn):
    cursor = conn.cursor()
    for redditor in redditors_yet_to_convert:
        if redditor in redditors_with_flair:
            cursor.execute(
                "UPDATE user_flairs_dms SET has_converted=1 WHERE redditor_name='{}'".format(redditor))

    conn.commit()


def updateDMConvert(subreddit):
    conn = sqlite3.connect('el_flairs.db')

    redditors_yet_to_convert = getRedditorsYetToConvert(conn)
    redditors_with_flair = getRedditorsWithFlair(subreddit)

    updateConvertedRedditors(redditors_with_flair,
                             redditors_yet_to_convert, conn)

    conn.close()


if __name__ == "__main__":
    flairs_dict = dict()

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Post Game Thread Generator Script")

    subreddit = reddit.subreddit("Euroleague")

    updateDMConvert(subreddit)
