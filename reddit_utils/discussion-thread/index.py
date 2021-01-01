from collections import namedtuple
from datetime import date, timedelta, datetime
from reddit_utils.subreddit import get_subreddit, submit_text_post, get_test_subreddit
from reddit_utils.helpers import double_newline_join, bold
from reddit_utils.constants import HORIZONTAL_LINE
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


class Game:
    def __init__(self, home_team, away_team, event_time):
        self.home_team = home_team
        self.away_team = away_team
        self.event_time = event_time

    @property
    def home_team(self):
        return self._home_team

    @home_team.setter
    def home_team(self, home_team):
        self._home_team = home_team

    @property
    def away_team(self):
        return self._away_team

    @away_team.setter
    def away_team(self, away_team):
        self._away_team = away_team

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, event_time):
        # timedelta is used to generate CET datetime
        self._event_time = event_time + timedelta(hours=1)

    def __repr__(self):
        event_time_repr = self.event_time.strftime("%b %d %H:%M")
        return '{} - {} | {} CET'.format(self.home_team, self.away_team, event_time_repr)

    def __str__(self):
        event_time_repr = self.event_time.strftime("%b %d %H:%M")
        return '{} - {} | {} CET'.format(self.home_team, self.away_team, event_time_repr)


def get_current_week_interval():
    week_start = datetime.combine(date.today(), datetime.min.time())
    week_end = datetime.combine(
        week_start + timedelta((6-week_start.weekday()) % 7), datetime.max.time())

    return (week_start, week_end)


def get_competitions():
    CompTuple = namedtuple(
        'comp_tuple', 'fs_link full_name small_name country standings')

    acb_tuple = CompTuple(
        'https://www.flashscore.com/basketball/spain/acb/fixtures/', 'Liga ACB', 'ACB', 'Spain', 'https://www.flashscore.com/basketball/spain/acb/standings/')
    lnb_tuple = CompTuple(
        'https://www.flashscore.com/basketball/france/lnb/fixtures/', 'LNB Pro A', 'LNB', 'France', 'https://www.flashscore.com/basketball/france/lnb/standings/')
    lega_a_tuple = CompTuple(
        'https://www.flashscore.com/basketball/italy/lega-a/fixtures/', 'Lega Basket Serie A', 'LBA', 'Italy', 'https://www.flashscore.com/basketball/italy/lega-a/standings/')
    bbl_tuple = CompTuple(
        'https://www.flashscore.com/basketball/germany/bbl/fixtures/', 'Basketball-Bundesliga', 'BBL', 'Germany', 'https://www.flashscore.com/basketball/germany/bbl/standings/')
    bsl_tuple = CompTuple(
        'https://www.flashscore.com/basketball/turkey/super-ligi/fixtures/', 'Turkish Basketbol Super Ligi', 'BSL', 'Turkey', 'https://www.flashscore.com/basketball/turkey/super-ligi/standings/')
    gbl_tuple = CompTuple(
        'https://www.flashscore.com/basketball/greece/basket-league/fixtures/', 'Greek A1 Basketball League', 'GBL', 'Greece', 'https://www.flashscore.com/basketball/greece/basket-league/standings/')
    wl_tuple = CompTuple(
        'https://www.flashscore.com/basketball/israel/super-league/fixtures/', 'Israeli Basketbell Premier League', 'IBPL', 'Israel', 'https://www.flashscore.com/basketball/israel/super-league/standings/')
    lkl_tuple = CompTuple(
        'https://www.flashscore.com/basketball/lithuania/lkl/fixtures/', 'Lietuvos krepšinio lyga', 'LKL', 'Lithuania', 'https://www.flashscore.com/basketball/lithuania/lkl/standings/')
    vtb_tuple = CompTuple(
        'https://www.flashscore.com/basketball/russia/vtb-united-league/fixtures/', 'VTB United League', 'VTB', None, 'https://www.flashscore.com/basketball/russia/vtb-united-league/standings/')
    aba_tuple = CompTuple(
        'https://www.flashscore.com/basketball/europe/aba-league/fixtures/', 'ABA Liga', 'ABA', None, 'https://www.flashscore.com/basketball/europe/aba-league/standings/')
    bcl_tuple = CompTuple(
        'https://www.flashscore.com/basketball/europe/champions-league/fixtures/', 'Basketball Champions League', 'BCL', None, 'https://www.flashscore.com/basketball/europe/champions-league/standings/')
    fec_tuple = CompTuple(
        'https://www.flashscore.com/basketball/europe/fiba-europe-cup/', 'FIBA Europe Cup', 'FEC', None, 'https://www.flashscore.com/basketball/europe/fiba-europe-cup/standings/')

    competitions = list()
    competitions.append([acb_tuple, lnb_tuple])
    competitions.append([lega_a_tuple, bbl_tuple])
    competitions.append([bsl_tuple, gbl_tuple])
    competitions.append([wl_tuple, lkl_tuple])
    competitions.append([vtb_tuple, aba_tuple])
    competitions.append([bcl_tuple, fec_tuple])

    return competitions


def get_event_time_date(event_time, week_start_date, week_end_date):
    #TODO: Refactor
    if week_start_date.year != week_end_date.year:
        event_month = int(event_time[3:5])
        if event_month == 12:
            date_parsed = '{}.{}'.format(week_start_date.year, event_time)
        else:
            date_parsed = '{}.{}'.format(week_end_date.year, event_time)
    else:
        date_parsed = '{}.{}'.format(week_start_date.year, event_time)

    return datetime.strptime(date_parsed, "%Y.%d.%m. %H:%M")


def get_competition_games(driver, fs_link: str, week_interval: tuple):
    driver.get(fs_link)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    competition_games = list()

    all_events = soup.find_all('div', class_='event__match')

    for event in all_events:
        if event.find('div', class_='lineThrough'):
            continue

        event_time = event.find('div', class_='event__time').text

        week_start_date = week_interval[0]
        week_end_date = week_interval[1]

        event_time_date = get_event_time_date(
            event_time, week_start_date, week_end_date)

        if week_start_date <= event_time_date <= week_end_date:
            home_team = event.find(
                'div', class_='event__participant--home').text
            away_team = event.find(
                'div', class_='event__participant--away').text

            game = Game(home_team, away_team, event_time_date)
            competition_games.append(game)

    return competition_games


def read_boilerplate_from_file(filename):
    with open(filename, mode='r') as bp:
        return bp.read()


def build_competition_group_thread(subreddit, week_start: str, week_end: str, group_list: list):
    comp_small_names = list()
    comp_full_names = list()
    markdown_list = list()

    # List value to infer if the text to be prepended includes information about cups/lower leagues
    # This does not apply to competitions whose country is None (i.e., VTB and ABA)
    # In the future, we might add support for countries related to clubs in those leagues
    countries = list()

    for competition, games in group_list:
        comp_small_names.append(competition.small_name)
        comp_full_names.append(competition.full_name)
        markdown_list.append(
            '{}- [Standings]({})'.format(bold(competition.full_name), competition.standings))

        if len(games) > 0:
            markdown_list.extend([str(g) for g in games])
        else:
            markdown_list.append('No games scheduled this week')

        markdown_list.append(HORIZONTAL_LINE)

        if competition.country is not None:
            countries.append(competition.country)

    small_names_join = '/'.join(comp_small_names)
    long_names_join = '/'.join(comp_full_names)

    # Depending upon the number of countries in the group, different solutions
    # 0 - unformatted boilerplate (no domestic leagues/lower divisions)
    # 1 - no '/' join in formatted boilerplate
    # >1 - '/' join countries in formatted boilerplate
    if len(countries) > 0:
        bp = read_boilerplate_from_file('group_pre_cup.txt')
        if len(countries) > 1:
            countries_markdown = '/'.join(countries)
            markdown_pre = bp.format(
                competitions=long_names_join, countries=countries_markdown)
        else:
            markdown_pre = bp.format(
                competitions=long_names_join, countries=countries[0])
    else:
        bp = read_boilerplate_from_file('group_pre.txt')
        markdown_pre = bp.format(competitions=long_names_join)

    # Technique used to "prepend" the preceeding elements in the markdown
    markdown_list = [markdown_pre, HORIZONTAL_LINE, *markdown_list]

    title = '{competitions} Discussion Thread [{week_start} - {week_end}]'.format(
        week_start=week_start, week_end=week_end, competitions=small_names_join)

    note = "{}Asking for or sharing illegal streams is NOT allowed!".format(
        bold("Note:"))
    markdown = double_newline_join([*markdown_list, note])

    return submit_text_post(
        subreddit, title, markdown, suggested_sort='new')


def build_general_discussion_thread(subreddit, week_start: str, week_end: str):
    title = 'Weekly Discussion Thread [{} - {}]'.format(week_start, week_end)
    markdown = 'Will be updated'

    return submit_text_post(
        subreddit, title, markdown, sticky=True, suggested_sort='new')


def update_general_discussion_thread(submission, group_submissions):
    discussion_threads_markdown = ["[{}]({})".format(
        sub.title, sub.url) for sub in group_submissions]

    with open('general.txt', mode='r') as bp:
        boilerplate = bp.read()

    markdown = boilerplate.format(
        group_links=double_newline_join(discussion_threads_markdown))

    return submission.edit(markdown)


def build_discussion_threads(subreddit, driver, competition_groups: list, week_interval: tuple):
    def convert_date_to_str(day):
        return day.strftime("%b %d")

    week_start = convert_date_to_str(week_interval[0])
    week_end = convert_date_to_str(week_interval[1])

    general_discussion_submission = build_general_discussion_thread(
        subreddit, week_start, week_end)

    group_submissions = list()

    for group in competition_groups:
        group_list = list()
        for competition in group:
            competition_games = get_competition_games(
                driver, competition.fs_link, week_interval)

            competition_tuple = (competition, competition_games)
            group_list.append(competition_tuple)

        group_submission = build_competition_group_thread(
            subreddit, week_start, week_end, group_list)
        group_submissions.append(group_submission)

    update_general_discussion_thread(
        general_discussion_submission, group_submissions)


def main():
    competition_groups = get_competitions()

    week_interval = get_current_week_interval()

    subreddit = get_subreddit()

    driver = webdriver.Firefox()

    build_discussion_threads(
        subreddit, driver, competition_groups, week_interval)

    driver.close()


if __name__ == '__main__':
    main()
