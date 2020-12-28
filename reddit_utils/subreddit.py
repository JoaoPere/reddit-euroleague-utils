from reddit_utils.prepare_dot_env import get_bot_credentials, get_test_credentials
import os
import praw


def get_subreddit():
    get_bot_credentials()
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/EuroLeague Master Script")

    reddit.validate_on_submit = True
    subreddit = reddit.subreddit('Euroleague')

    return subreddit


def get_test_subreddit():
    get_test_credentials()
    reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                         client_secret=os.getenv("REDDIT_APP_SECRET"),
                         password=os.getenv("REDDIT_PASSWORD"),
                         username=os.getenv("REDDIT_ACCOUNT"),
                         user_agent="r/thekingpin")

    reddit.validate_on_submit = True
    subreddit = reddit.subreddit('thekingpin')

    return subreddit


def submit_text_post(subreddit, title, markdown, *args, **kwargs):
    submission = subreddit.submit(title=title, selftext=markdown)

    sticky = kwargs.get('sticky', False)
    if sticky:
        submission.mod.sticky()

    suggested_sort = kwargs.get('suggested_sort', None)
    if suggested_sort is not None:
        submission.mod.suggested_sort(suggested_sort)

    flair_text = kwargs.get('flair_text', None)
    if flair_text is not None:
        flair_choices = submission.flair.choices()
        template_id = next(x for x in flair_choices if x['flair_text'].replace(
            ':', '') == flair_text)['flair_template_id']
        submission.flair.select(template_id)

    return submission
