from prepare_dot_env import prepareDotEnv
from team_structs import team_info_by_official
import requests
from bs4 import BeautifulSoup
import sys
from collections import namedtuple
from datetime import datetime, timezone, tzinfo
import praw
import os

sys.path.append('..')


CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'
DOUBLE_NEWLINE = '\n\n'

prepareDotEnv()

reddit = praw.Reddit(client_id=os.getenv("REDDIT_APP_ID"),
                     client_secret=os.getenv("REDDIT_APP_SECRET"),
                     password=os.getenv("REDDIT_PASSWORD"),
                     username=os.getenv("REDDIT_ACCOUNT"),
                     user_agent="r/EuroLeague Post Game Thread Generator Script")

el_sub = reddit.subreddit('Euroleague')

# Since new returns an iterator, it's obligatory to convert to list so that elements are not consumed
new_submissions = list(el_sub.new(limit=100))


def appendTableDelimitors(content):
    return TABLE_DELIM + content + TABLE_DELIM

# Returns the href to the result thread


def getResultThread(home_team, away_team, competition_stage, round_or_game):
    reddit_home_team = team_info_by_official.get(home_team).reddit
    reddit_away_team = team_info_by_official.get(away_team).reddit

    title_to_find = 'Post-Match Thread: {home_team} - {away_team} [EuroLeague {competition_stage}, {round_or_game}]'.format(
        home_team=reddit_home_team, away_team=reddit_away_team, competition_stage=competition_stage, round_or_game=round_or_game)

    for submission in new_submissions:
        if submission.title == title_to_find:
            return submission.url

    return None


class PlayoffMatchUp():
    def __init__(self, team_1, team_2):
        self._team_1 = team_1  # Has HCA in the list
        self._team_2 = team_2

        self.games = []

    @property
    def team_1(self):
        return self._team_1

    @property
    def team_2(self):
        return self._team_2

    def __eq__(self, other):
        if not isinstance(other, PlayoffMatchUp):
            raise Exception

        return all(t in [other.team_1, other.team_2] for t in [self.team_1, self.team_2])

    def __repr__(self):
        repr_games = [repr(g) for g in self.games]

        reddit_table_head = appendTableDelimitors(
            TABLE_DELIM.join(['GAME', 'HOME', 'AWAY', 'RESULT']))
        reddit_cell_allignment = appendTableDelimitors(
            TABLE_DELIM.join([CELL_ALLIGNMENT] * 4))

        final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])

        return NEWLINE.join([final_table, *repr_games])

    def addGame(self, game):
        self.games.append(game)


class Game():
    def __init__(self, comp_stage, game_str, team_1, team_2, score=None, bool_md_round=True):
        self.score = score
        self.comp_stage = comp_stage

        self.game_str = game_str
        self.game_number = [int(s)
                            for s in self.game_str.split() if s.isdigit()][0]

        self.home_team = team_1
        self.away_team = team_2

        self.bool_md_round = bool_md_round

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    def __repr__(self):
        submission_url = getResultThread(
            self.home_team, self.away_team, self.comp_stage, self.game_str)

        result = "[{home_team_score}-{away_team_score}]({submission_url})".format(home_team_score=str(
            self.score[0]), away_team_score=str(self.score[1]), submission_url=submission_url)
        #result = "{}-{}".format(str(self.score[0]), str(self.score[1]))

        home_team_3lmd = team_info_by_official.get(self.home_team).letter3_md
        away_team_3lmd = team_info_by_official.get(self.away_team).letter3_md

        # [>game, >home_team, away_team, >result]

        game_or_round_md = str(self.game_number) if self.bool_md_round else ""

        row_markdown = appendTableDelimitors(TABLE_DELIM.join(
            [game_or_round_md, home_team_3lmd, away_team_3lmd, result]))
        return row_markdown

# Works solely for regular season


def getResultsTableForRegularSeason(week):
    r = requests.get(
        'https://www.euroleague.net/main/results?gamenumber={}&seasoncode=E2020'.format(week))

    soup = BeautifulSoup(r.text, 'html.parser')

    reddit_table_head = appendTableDelimitors(
        TABLE_DELIM.join(['ROUND', 'HOME', 'AWAY', 'RESULT']))
    reddit_cell_allignment = appendTableDelimitors(
        TABLE_DELIM.join([CELL_ALLIGNMENT] * 4))

    final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])

    # Result in 2nd element
    livescores = soup.find_all("div", class_="livescore")

    schedule_html = livescores[1]

    schedule_html_games = schedule_html.find_all("div", class_="game")

    gc_title_spans = soup.find('div', class_='gc-title').find_all('span')
    comp_stage = gc_title_spans[1].text
    round_str = gc_title_spans[2].text

    for idx, html_game in enumerate(schedule_html_games):
        both_clubs = html_game.find_all("div", class_="club")

        home_team_official = both_clubs[0].find("span", class_="name").text
        away_team_official = both_clubs[1].find("span", class_="name").text

        home_team_score = both_clubs[0].find(
            "span", class_="score").attrs['data-score']
        away_team_score = both_clubs[1].find(
            "span", class_="score").attrs['data-score']

        # Only assign to the first row of the table - Reddit markdown syntax related
        bool_md_round = True if idx == 0 else False

        game = Game(comp_stage, round_str, home_team_official,
                    away_team_official, (home_team_score, away_team_score), bool_md_round)
        final_table = NEWLINE.join([final_table, repr(game)])

    final_table = NEWLINE.join(
        [final_table, '**Note:** Access the post-match threads by clicking in the result'])

    return final_table


def getResultsTableForPlayoffs(week):
    week_int = int(week)
    week_loop = 31

    matchup_list = list()

    while week_loop <= week_int:
        r = requests.get(
            'https://www.euroleague.net/main/results?gamenumber={}&seasoncode=E2019'.format(week_loop))
        soup = BeautifulSoup(r.text, 'html.parser')

        # Result in 2nd element
        livescores = soup.find_all(
            "div", class_="game-center-container-results col-md-4 col-lg-3")

        schedule_html = livescores[0]

        schedule_html_games = schedule_html.find_all("div", class_="game")

        gc_title_spans = soup.find('div', class_='gc-title').find_all('span')
        comp_stage = gc_title_spans[1].text
        game_str = gc_title_spans[2].text

        for idx, html_game in enumerate(schedule_html_games):
            both_clubs = html_game.find_all("div", class_="club")

            home_team_official = both_clubs[0].find("span", class_="name").text
            away_team_official = both_clubs[1].find("span", class_="name").text

            # TODO: Check if scores were changed. I believe the data-score attribute was added this year, so for testing purposes scores are mock objects
            home_team_score = both_clubs[0].find(
                "span", class_="score").attrs['data-score']
            #home_team_score = str(90)

            away_team_score = both_clubs[1].find(
                "span", class_="score").attrs['data-score']
            #away_team_score = str(91)

            # Needs refactoring -> look into a method that simplifies this
            matchup_game = PlayoffMatchUp(
                home_team_official, away_team_official)
            if not matchup_game in matchup_list:
                matchup_list.append(matchup_game)

            existing_matchup = next(
                (m for m in matchup_list if m == matchup_game), None)

            game = Game(comp_stage, game_str, home_team_official,
                        away_team_official, (home_team_score, away_team_score))
            existing_matchup.addGame(game)

        week_loop += 1

    return DOUBLE_NEWLINE.join([repr(m) for m in matchup_list])


def getResultsTable(week):
    week_int = int(week)
    if week_int == 0:
        return "**Round 1 hasn't finished. No results available right now**"
    if week_int < 31:
        return getResultsTableForRegularSeason(week)
    else:
        return getResultsTableForPlayoffs(week)


if __name__ == '__main__':
    print(getResultsTable(sys.argv[1]))
