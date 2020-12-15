from reddit_utils import prepare_dot_env
from reddit_utils.subreddit import get_subreddit
import praw
import os
import sqlite3


def get_redditors_yet_to_convert(conn):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT redditor_name FROM user_flairs_dms WHERE has_converted=0")
    all_users = cursor.fetchall()

    return [user[0] for user in all_users]


def get_redditors_with_flair(subreddit):
    return [template['user'].name
            for template in subreddit.flair(limit=None)]


def update_converted_redditors(redditors_with_flair, redditors_yet_to_convert, conn):
    cursor = conn.cursor()
    for redditor in redditors_yet_to_convert:
        if redditor in redditors_with_flair:
            cursor.execute(
                "UPDATE user_flairs_dms SET has_converted=1 WHERE redditor_name='{}'".format(redditor))

    conn.commit()


def update_converted_dms(subreddit):
    conn = sqlite3.connect('el_flairs.db')

    redditors_yet_to_convert = get_redditors_yet_to_convert(conn)
    redditors_with_flair = get_redditors_with_flair(subreddit)

    update_converted_redditors(redditors_with_flair,
                               redditors_yet_to_convert, conn)

    conn.close()


def main():
    subreddit = get_subreddit()

    update_converted_dms(subreddit)


if __name__ == "__main__":
    main()
