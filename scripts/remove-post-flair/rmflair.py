import praw

reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
                     client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
                     password='tQ#1O&4k32Xy',
                     user_agent='Euroleague Post-Game Thread Script',
                     username='Al-Farrekt-Aminu')

el_sub = reddit.subreddit('Euroleague')

for submission in el_sub.stream.submissions():
    print(submission) 	