from reddit_utils.team_structs import team_info_by_official
import reddit_utils.helpers as rh
from datetime import datetime, timezone, tzinfo
from bs4 import BeautifulSoup
import requests
import praw
import sys
import argparse


def get_schedule_table(week):
    r = requests.get(
        'https://www.euroleague.net/main/results?gamenumber={}&seasoncode=E2020'.format(week))

    soup = BeautifulSoup(r.text, 'html.parser')

    final_table = rh.get_reddit_table_head_and_cell_alignment(
        ['ROUND', 'DATE', 'HOME', 'AWAY', 'TIME'])

    # Result in 2nd element
    livescores = soup.find_all("div", class_="livescore")

    schedule_html = livescores[1]

    schedule_html_games = schedule_html.find_all("div", class_="game")

    cond_day = 0

    for idx, html_game in enumerate(schedule_html_games):
        both_clubs = html_game.find_all("div", class_="club")

        home_team_name = team_info_by_official.get(
            str(both_clubs[0].find("span", class_="name").get_text())).letter3_md
        away_team_name = team_info_by_official.get(
            str(both_clubs[1].find("span", class_="name").get_text())).letter3_md

        el_round = str(week) if idx == 0 else ""
        game_date = html_game.find("span", class_="date")
        if game_date is not None:
            game_date_text = game_date.get_text()

            # Removes "CET" from the string
            game_date_text = game_date_text.strip()[:len(game_date_text) - 4]
            game_date_text = datetime.strptime(game_date_text, "%B %d %H:%M")

            el_date = game_date_text.strftime("%b %d") if idx == 0 or (
                idx > 0 and int(game_date_text.day) != cond_day) else ""
            cond_day = game_date_text.day
            row_markdown = rh.build_table_delimitors(
                [el_round, el_date, home_team_name, away_team_name, game_date_text.strftime("%H:%M")])
        else:
            el_date = ''
            row_markdown = rh.build_table_delimitors(
                [el_round, el_date, home_team_name, away_team_name, 'PP'])

        final_table = rh.newline_join([final_table, row_markdown])

    # Add note
    final_table = rh.newline_join(
        [final_table, '**Note:** All CET times // PP = Postponed'])
    return final_table


def main():
    parser = argparse.ArgumentParser(description='Sidebar schedule creator')
    parser.add_argument('week', metavar='W', type=str)

    args = parser.parse_args()
    print(get_schedule_table(args.week))


if __name__ == '__main__':
    main()
