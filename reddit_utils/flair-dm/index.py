from reddit_utils.subreddit import get_subreddit
import sys
import praw
import os
import time
import sqlite3


def get_comment_and_submission_streams(subreddit):
    comment_stream = subreddit.stream.comments(
        pause_after=-1, skip_existing=True)
    submission_stream = subreddit.stream.submissions(
        pause_after=-1, skip_existing=True)

    return comment_stream, submission_stream


def get_dm_boilerplate():
    with open('dm_boilerplate.txt', mode='r') as bp:
        return bp.read()


def get_users_with_flairs(subreddit):
    return [template['user'] for template in subreddit.flair(limit=None)]


def send_direct_message_to_redditor(conn, users_that_have_been_sent_dms, entry_author, title, boilerplate):
    while True:
        try:
            # Sends the Reddit message to the entry author
            entry_author.message(title, boilerplate.format(
                redditor_name=entry_author.name), from_subreddit="Euroleague")

            entry_author_name = entry_author.name

            # Inserts the redditor name into the database
            insert_user_that_has_been_sent_dm(conn, entry_author_name)

            # Appends the new redditor to memory and returns the value
            users_that_have_been_sent_dms.append(entry_author_name)

            print("Sent DM to: {}".format(entry_author_name))

            # Has to return something to break the cycle
            return None
        except Exception:
            print('Unable to send PM. Trying again')

            time.sleep(5)


def handle_reddit_streams(subreddit):
    conn = sqlite3.connect('el_flairs.db')

    users_that_have_been_sent_dms = get_users_that_have_already_been_sent_dms(
        conn)

    print('Users that have already been sent DMs: {}'.format(
        ', '.join(users_that_have_been_sent_dms)))
    print()

    comment_stream, submission_stream = get_comment_and_submission_streams(
        subreddit)

    dm_boilerplate = get_dm_boilerplate()
    dm_title = "Welcome to r/Euroleague! Fancy representing your team?"

    print("Starting to listen to the new entry streams")
    print()

    while True:
        try:
            for comment in comment_stream:
                if comment is None:
                    break

                handle_new_entry(
                    subreddit, conn, users_that_have_been_sent_dms, comment, dm_title, dm_boilerplate)
            for submission in submission_stream:
                if submission is None:
                    break
                handle_new_entry(subreddit, conn, users_that_have_been_sent_dms,
                                 submission, dm_title, dm_boilerplate)
        except Exception:
            print('Unable to connect to PRAW. Trying again')
            comment_stream, submission_stream = get_comment_and_submission_streams(
                subreddit)

            time.sleep(5)


def handle_new_entry(subreddit, conn, users_that_have_been_sent_dms, entry, title, boilerplate):
    users_with_flairs = get_users_with_flairs(subreddit)

    entry_author = entry.author
    entry_author_name = entry_author.name

    if entry_author_name not in users_with_flairs and entry_author_name not in users_that_have_been_sent_dms:
        send_direct_message_to_redditor(
            conn, users_that_have_been_sent_dms, entry_author, title, boilerplate)


def get_users_that_have_already_been_sent_dms(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_flairs_dms")
    all_users = cursor.fetchall()

    return [user[0] for user in all_users]


def insert_user_that_has_been_sent_dm(conn, redditor_name):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_flairs_dms VALUES ('{}', 0);".format(redditor_name))
    conn.commit()


def main():
    subreddit = get_subreddit()

    handle_reddit_streams(subreddit)


if __name__ == "__main__":
    main()
