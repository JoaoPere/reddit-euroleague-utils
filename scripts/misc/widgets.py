import praw

reddit = praw.Reddit(client_id='DqcFxX1SwJkLDQ',
                     client_secret='mbFOhcHP9sxbs5PmnoojCqjxDm0',
                     password='tQ#1O&4k32Xy',
                     user_agent='Euroleague Post-Game Thread Script',
                     username='Al-Farrekt-Aminu')

el_sub = reddit.subreddit('Euroleague')

widgets = el_sub.widgets
widgets.progressive_images = True

for widget in widgets.sidebar[:-1]:
	print(widget.text)