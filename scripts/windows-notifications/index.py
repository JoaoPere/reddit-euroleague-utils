import sys
import praw
import re
import os
from win10toast import ToastNotifier
import webbrowser

sys.path.append('..')

from prepare_dot_env import prepareDotEnv

def openRedditSubmission(url):
    return webbrowser.open_new_tab(url)

if __name__ == '__main__':
    prepareDotEnv()

    me = os.getenv("REDDIT_ACCOUNT")

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                    client_secret=os.getenv("REDDIT_APP_SECRET"),
                    password=os.getenv("REDDIT_PASSWORD"),
                    username=me,
                    user_agent="r/EuroLeague Sidebar Update Script")

    el_sub = reddit.subreddit('Euroleague')

    toaster = ToastNotifier()
    for submission in el_sub.stream.submissions(skip_existing=True):  
        submission_title = submission.title
        submission_author = submission.author.name
        submission_by_author = 'by {}'.format(submission_author)

        # There's no comments_url in Submission, so we manually create it through the ID.
        submission_id = submission.id
        submission_url = 'https://old.reddit.com/r/Euroleague/comments/{}/'.format(submission_id)

        print('Title: {}'.format(submission_title))
        print('Author: {}'.format(submission_author))
        print('URL: {}'.format(submission_url))
        print()
        
        # Do not show if it is my own
        if not submission_author == me:
            toaster.show_toast(title=submission_title, msg=submission_by_author, icon_path='reddit.ico', duration=5, threaded=False, callback_on_click=lambda: openRedditSubmission(submission_url))
