from reddit_utils.team_structs import team_info_by_official
import requests
from bs4 import BeautifulSoup
import praw
import sys
from datetime import datetime, timezone, tzinfo

sys.path.append('..')


CELL_ALLIGNMENT = ':-:'
TABLE_DELIM = '|'
NEWLINE = '\n'


def appendTableDelimitors(content):
    return TABLE_DELIM + content + TABLE_DELIM


def getScheduleTable(week):
    r = requests.get(
        'https://www.euroleague.net/main/results?gamenumber={}&seasoncode=E2020'.format(week))

    soup = BeautifulSoup(r.text, 'html.parser')

    reddit_table_head = appendTableDelimitors(
        TABLE_DELIM.join(['ROUND', 'DATE', 'HOME', 'AWAY', 'TIME']))
    reddit_cell_allignment = appendTableDelimitors(
        TABLE_DELIM.join([CELL_ALLIGNMENT] * 5))

    final_table = NEWLINE.join([reddit_table_head, reddit_cell_allignment])

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
            row_markdown = appendTableDelimitors(TABLE_DELIM.join(
                [el_round, el_date, home_team_name, away_team_name, game_date_text.strftime("%H:%M")]))
        else:
            el_date = ''
            row_markdown = appendTableDelimitors(TABLE_DELIM.join(
                [el_round, el_date, home_team_name, away_team_name, 'PP']))

        final_table = NEWLINE.join([final_table, row_markdown])

    # Add note
    final_table = NEWLINE.join(
        [final_table, '**Note:** All CET times // PP = Postponed'])
    return final_table


if __name__ == '__main__':
    print(getScheduleTable(sys.argv[1]))
