from reddit_utils import prepare_dot_env
import time
import webbrowser
from win10toast import ToastNotifier
import os
import praw
import sys
import prawcore


SUBREDDIT_NAME = 'Euroleague'


def getCommentAndSubmissionStreams(subreddit):
    comment_stream = subreddit.stream.comments(
        pause_after=-1, skip_existing=True)
    submission_stream = subreddit.stream.submissions(
        pause_after=-1, skip_existing=True)

    return comment_stream, submission_stream


def handleRedditStreams(subreddit):
    comment_stream, submission_stream = getCommentAndSubmissionStreams(
        subreddit)

    toaster = ToastNotifier()

    while True:
        try:
            for comment in comment_stream:
                if comment is None:
                    break
                handleNewComment(comment, toaster)
            for submission in submission_stream:
                if submission is None:
                    break
                handleNewSubmission(submission, toaster)
        except Exception:
            print('Unable to connect to PRAW. Trying again in 30 seconds.')
            print('')
            # Experimental, wasn't recovering previously
            comment_stream, submission_stream = getCommentAndSubmissionStreams(
                subreddit)
            time.sleep(30)


def handleNewComment(comment, toaster):
    comment_submission_title = comment.submission.title
    comment_author = comment.author.name
    comment_by_author = 'Comment created by {}'.format(comment_author)
    comment_body = comment.body

    comment_permalink = comment.permalink
    comment_url = 'https://old.reddit.com{}'.format(comment_permalink)

    print('# COMMENT #')
    print('Title: {}'.format(comment_submission_title))
    print('Author: {}'.format(comment_author))
    print('URL: {}'.format(comment_url))
    print('Body: {}'.format(comment_body))
    print()

    toaster.show_toast(title=comment_submission_title, msg=comment_by_author, icon_path='reddit.ico',
                       duration=5, threaded=False, callback_on_click=lambda: openRedditSubmission(comment_url))


def handleNewSubmission(submission, toaster):
    submission_title = submission.title
    submission_author = submission.author.name
    submission_by_author = 'Submission created by {}'.format(submission_author)

    # There's no comments_url in Submission, so we manually create it through the ID.
    submission_id = submission.id
    submission_url = 'https://old.reddit.com/r/{}/comments/{}/'.format(
        SUBREDDIT_NAME, submission_id)

    print('# SUBMISSION #')
    print('Title: {}'.format(submission_title))
    print('Author: {}'.format(submission_author))
    print('URL: {}'.format(submission_url))
    print()
    toaster.show_toast(title=submission_title, msg=submission_by_author, icon_path='reddit.ico',
                       duration=5, threaded=False, callback_on_click=lambda: openRedditSubmission(submission_url))


def openRedditSubmission(url):
    return webbrowser.open_new_tab(url)


if __name__ == '__main__':
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Sidebar Update Script")

    el_sub = reddit.subreddit(SUBREDDIT_NAME)

    handleRedditStreams(el_sub)
