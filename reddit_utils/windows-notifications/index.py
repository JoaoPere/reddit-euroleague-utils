from reddit_utils.subreddit import get_subreddit
import time
import webbrowser
from win10toast import ToastNotifier
import os
import praw
import sys
import prawcore


def get_comment_and_submission_streams(subreddit):
    comment_stream = subreddit.stream.comments(
        pause_after=-1, skip_existing=True)
    submission_stream = subreddit.stream.submissions(
        pause_after=-1, skip_existing=True)

    return comment_stream, submission_stream


def handle_reddit_streams(subreddit):
    comment_stream, submission_stream = get_comment_and_submission_streams(
        subreddit)

    toaster = ToastNotifier()

    while True:
        try:
            for comment in comment_stream:
                if comment is None:
                    break
                handle_new_comment(comment, toaster)
            for submission in submission_stream:
                if submission is None:
                    break
                handle_new_submission(submission, toaster)
        except Exception:
            print('Unable to connect to PRAW. Trying again in 30 seconds.')
            print('')
            # Experimental, wasn't recovering previously
            comment_stream, submission_stream = get_comment_and_submission_streams(
                subreddit)
            time.sleep(30)


def handle_new_comment(comment, toaster):
    comment_by_author = 'Comment created by {}'.format(comment.author.name)
    comment_url = 'https://old.reddit.com{}'.format(comment.permalink)

    print('# COMMENT #')
    print('Title: {}'.format(comment.submission.title))
    print('Author: {}'.format(comment.author.name))
    print('URL: {}'.format(comment_url))
    print('Body: {}'.format(comment.body))
    print()

    toaster.show_toast(title=comment.submission.title, msg=comment_by_author, icon_path='reddit.ico',
                       duration=5, threaded=False, callback_on_click=lambda: open_subreddit_submission(comment_url))


def handle_new_submission(submission, toaster):
    submission_by_author = 'Submission created by {}'.format(
        submission.author.name)

    # There's no comments_url in Submission, so we manually create it through the ID.
    submission_url = 'https://old.reddit.com/r/Euroleague/comments/{}/'.format(
        submission.id)

    print('# SUBMISSION #')
    print('Title: {}'.format(submission.title))
    print('Author: {}'.format(submission.author.name))
    print('URL: {}'.format(submission_url))
    print()
    toaster.show_toast(title=submission.title, msg=submission_by_author, icon_path='reddit.ico',
                       duration=5, threaded=False, callback_on_click=lambda: open_subreddit_submission(submission_url))


def open_subreddit_submission(url):
    return webbrowser.open_new_tab(url)


def main():
    subreddit = get_subreddit()

    handle_reddit_streams(subreddit)


if __name__ == '__main__':
    main()
