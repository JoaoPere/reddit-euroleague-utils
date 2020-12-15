from reddit_utils.team_structs import team_info_by_official
import reddit_utils.helpers as rh
from bs4 import BeautifulSoup
from datetime import datetime, timezone, tzinfo
import requests
import praw
import sys
import argparse


def get_results_table(week):
    r = requests.get(
        'https://www.euroleague.net/main/results?gamenumber={}&phasetypecode=RS&seasoncode=E2020'.format(week))

    soup = BeautifulSoup(r.text, 'html.parser')

    final_table = rh.get_reddit_table_head_and_cell_alignment(
        ['ROUND', 'HOME', 'AWAY', 'RESULT'])

    # Result in 2nd element
    livescores = soup.find_all("div", class_="livescore")

    schedule_html = livescores[1]

    schedule_html_games = schedule_html.find_all("div", class_="game")

    for idx, html_game in enumerate(schedule_html_games):
        both_clubs = html_game.find_all("div", class_="club")

        home_team_name = team_info_by_official.get(
            str(both_clubs[0].find("span", class_="name").get_text())).letter3_md
        home_team_score = both_clubs[0].find(
            "span", class_="score").attrs['data-score']

        away_team_name = team_info_by_official.get(
            str(both_clubs[1].find("span", class_="name").get_text())).letter3_md
        away_team_score = both_clubs[1].find(
            "span", class_="score").attrs['data-score']

        el_round = sys.argv[1] if idx == 0 else ""
        result = "[{}-{}]()".format(home_team_score,
                                    away_team_score) if home_team_score != '-' and away_team_score != '-' else 'POSTPONED'

        row_markdown = rh.build_table_delimitors(
            [el_round, home_team_name, away_team_name, result])

        final_table = rh.newline_join([final_table, row_markdown])

    return final_table


def main():
    parser = argparse.ArgumentParser(description='Sidebar results creator')
    parser.add_argument('week', metavar='W', type=str)

    args = parser.parse_args()
    print(get_results_table(args.week))


if __name__ == '__main__':
    main()
