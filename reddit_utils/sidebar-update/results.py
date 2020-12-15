from reddit_utils import prepare_dot_env
from reddit_utils.team_structs import team_info_by_official
from reddit_utils.subreddit import get_subreddit
import reddit_utils.helpers as rh
from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import datetime, timezone, tzinfo
import requests
import sys
import praw
import os
import argparse


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

        final_table = rh.get_reddit_table_head_and_cell_alignment(
            ['GAME', 'HOME', 'AWAY', 'RESULT'])

        return rh.newline_join([final_table, *repr_games])

    def add_game(self, game):
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

    def get_result_thread(self):
        reddit_home_team = team_info_by_official.get(self.home_team).reddit
        reddit_away_team = team_info_by_official.get(self.away_team).reddit

        title_to_find = 'Post-Match Thread: {home_team} - {away_team} [EuroLeague {competition_stage}, {round_or_game}]'.format(
            home_team=reddit_home_team, away_team=reddit_away_team, competition_stage=self.comp_stage, round_or_game=self.game_str)

        for submission in Game.submissions:
            if submission.title == title_to_find:
                return submission.url

        return None

    def __repr__(self):
        submission_url = self.get_result_thread()

        result = "[{home_team_score}-{away_team_score}]({submission_url})".format(home_team_score=str(
            self.score[0]), away_team_score=str(self.score[1]), submission_url=submission_url) if self.score[0] != '-' and self.score[1] != '-' else 'POSTPONED'

        home_team_3lmd = team_info_by_official.get(self.home_team).letter3_md
        away_team_3lmd = team_info_by_official.get(self.away_team).letter3_md

        game_or_round_md = str(self.game_number) if self.bool_md_round else ""

        row_markdown = rh.build_table_delimitors(
            [game_or_round_md, home_team_3lmd, away_team_3lmd, result])
        return row_markdown


def get_results_table_for_regular_season(week):
    r = requests.get(
        'https://www.euroleague.net/main/results?gamenumber={}&seasoncode=E2020'.format(week))

    soup = BeautifulSoup(r.text, 'html.parser')

    final_table = rh.get_reddit_table_head_and_cell_alignment(
        ['ROUND', 'HOME', 'AWAY', 'RESULT'])

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
        final_table = rh.newline_join([final_table, repr(game)])

    final_table = rh.newline_join(
        [final_table, '**Note:** Access the post-match threads by clicking in the result'])

    return final_table


def get_results_table_for_playoffs(week):
    week_int = int(week)
    week_loop = 31

    matchup_list = list()

    while week_loop <= week_int:
        r = requests.get(
            'https://www.euroleague.net/main/results?gamenumber={}&seasoncode=E2020'.format(week_loop))
        soup = BeautifulSoup(r.text, 'html.parser')

        # Result in 2nd element
        livescores = soup.find_all(
            "div", class_="game-center-container-results col-md-4 col-lg-3")

        schedule_html = livescores[0]

        schedule_html_games = schedule_html.find_all("div", class_="game")

        gc_title_spans = soup.find('div', class_='gc-title').find_all('span')
        comp_stage = gc_title_spans[1].text
        game_str = gc_title_spans[2].text

        for html_game in schedule_html_games:
            both_clubs = html_game.find_all("div", class_="club")

            home_team_official = both_clubs[0].find("span", class_="name").text
            away_team_official = both_clubs[1].find("span", class_="name").text

            home_team_score = both_clubs[0].find(
                "span", class_="score").attrs['data-score']

            away_team_score = both_clubs[1].find(
                "span", class_="score").attrs['data-score']

            matchup_game = PlayoffMatchUp(
                home_team_official, away_team_official)
            if not matchup_game in matchup_list:
                matchup_list.append(matchup_game)

            existing_matchup = next(
                (m for m in matchup_list if m == matchup_game), None)

            game = Game(comp_stage, game_str, home_team_official,
                        away_team_official, (home_team_score, away_team_score))
            existing_matchup.add_game(game)

        week_loop += 1

    return rh.double_newline_join([repr(m) for m in matchup_list])


def get_results_table(week):
    el_sub = get_subreddit()

    # Since new returns an iterator, it's obligatory to convert to list so that elements are not consumed
    Game.submissions = list(el_sub.new(limit=100))
    week_int = int(week)

    if week_int == 0:
        return "**Round 1 hasn't finished. No results available right now**"
    if week_int < 31:
        return get_results_table_for_regular_season(week)
    else:
        return get_results_table_for_playoffs(week)


def main():
    parser = argparse.ArgumentParser(description='Sidebar results creator')
    parser.add_argument('week', metavar='W', type=str)

    args = parser.parse_args()
    print(get_results_table(args.week))


if __name__ == '__main__':
    main()
