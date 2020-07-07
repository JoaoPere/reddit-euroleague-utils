import sys
import praw
import os
import time
import sqlite3

sys.path.append('..')

from prepare_dot_env import prepareDotEnvBot

def getCommentAndSubmissionStreams(subreddit):
    comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
    submission_stream = subreddit.stream.submissions(
        pause_after=-1, skip_existing=True)

    return comment_stream, submission_stream

def getDirectMessageBoilerplate():
    with open('dm_boilerplate.txt', mode='r') as bp:
        return bp.read()

def getUsersWithFlairs(subreddit):
    return [template['user'] for template in subreddit.flair(limit=None)]

def sendDirectMessageToRedditor(conn, users_that_have_been_sent_dms, entry_author, title, boilerplate):
    while True:
        try:
            # Sends the Reddit message to the entry author
            #entry_author.message(title, boilerplate.format(redditor_name=entry_author.name), from_subreddit="Euroleague")

            entry_author_name = entry_author.name

            # Inserts the redditor name into the database
            insertUserThatHasBeenSentDM(conn, entry_author_name)

            # Appends the new redditor to memory and returns the value
            users_that_have_been_sent_dms.append(entry_author_name)

            printUpdatedInformation(users_that_have_been_sent_dms)

            # Has to return something to break the cycle
            return None
        except Exception:
            print('Unable to send PM. Trying again')
            print('')

            time.sleep(5)

def printUpdatedInformation(users_that_have_been_sent_dms):
    print('Updated list of users that have been sent DMs: {}'.format(', '.join(users_that_have_been_sent_dms)))
    print()

def handleRedditStreams(subreddit):
    conn = sqlite3.connect('el_flairs.db')
    
    users_that_have_been_sent_dms = getUsersThatHaveAlreadyBeenSentDMs(conn)

    print('Users that have already been sent DMs: {}'.format(', '.join(users_that_have_been_sent_dms)))
    print()

    comment_stream, submission_stream = getCommentAndSubmissionStreams(
        subreddit)

    dm_boilerplate = getDirectMessageBoilerplate()
    dm_title = "Welcome to r/Euroleague! Fancy representing your team?"

    print("Starting to listen to the new entry streams")
    print()

    while True:
        try:
            for comment in comment_stream:
                if comment is None:
                    break

                handleNewEntry(subreddit, conn, users_that_have_been_sent_dms, comment, dm_title, dm_boilerplate)
            for submission in submission_stream:
                if submission is None:
                    break
                handleNewEntry(subreddit, conn, users_that_have_been_sent_dms, submission, dm_title, dm_boilerplate)
        except Exception:
            print('Unable to connect to PRAW. Trying again')
            print('')
            comment_stream, submission_stream = getCommentAndSubmissionStreams(
                subreddit)

            time.sleep(5)

def handleNewEntry(subreddit, conn, users_that_have_been_sent_dms, entry, title, boilerplate):
    users_with_flairs = getUsersWithFlairs(subreddit)
    
    entry_author = entry.author
    entry_author_name = entry_author.name

    if entry_author_name not in users_with_flairs and entry_author_name not in users_that_have_been_sent_dms:
        sendDirectMessageToRedditor(conn, users_that_have_been_sent_dms, entry_author, title, boilerplate)

def getUsersThatHaveAlreadyBeenSentDMs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_flairs_dms")
    all_users = cursor.fetchall()

    return [user[0] for user in all_users]

def insertUserThatHasBeenSentDM(conn, redditor_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_flairs_dms VALUES ('{}', 0);".format(redditor_name))
    conn.commit()

if __name__ == "__main__":
    prepareDotEnvBot()

    flairs_dict = dict()

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Post Game Thread Generator Script")

    subreddit = reddit.subreddit("Euroleague")

    handleRedditStreams(subreddit)