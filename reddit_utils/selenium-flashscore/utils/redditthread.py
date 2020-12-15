from reddit_utils import prepare_dot_env
from reddit_utils.team_structs import team_info_by_fs
import reddit_utils.constants as rc
import reddit_utils.helpers as rh
from reddit_utils.subreddit import submit_text_post
from utils.redditgamethread import RedditGameThread
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import praw
import re
import sys
import os

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=sys.maxsize))
s.mount('https://', HTTPAdapter(max_retries=sys.maxsize))


def get_quarter_scores_markdown(soup, home_team, away_team):
    quarter_table = soup.find(
        id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_PartialsStatsByQuarter_dgPartials")
    quarter_table_rows = quarter_table.find_all('tr')

    table_head_elements = [th.text.upper()
                           for th in quarter_table_rows[0].find_all('th')]
    final_table = rh.get_reddit_table_head_and_cell_alignment(
        table_head_elements)

    for idx, row in enumerate(quarter_table_rows[1:]):
        quarter_table_cols = row.find_all('td')
        quarter_table_cols = [ele.text.strip() for ele in quarter_table_cols]

        # Overrides the team name
        quarter_table_cols[0] = team_info_by_fs.get(
            home_team).full_md if idx == 0 else team_info_by_fs.get(away_team).full_md

        cols_markdown = rh.build_table_delimitors(quarter_table_cols)

        final_table = rh.newline_join([final_table, cols_markdown])

    return final_table


def get_tables_markdown(soup, home_team_name, away_team_name):
    home_away_tables = soup.find_all(id='tblPlayerPhaseStatistics')

    home_table = home_away_tables[0]
    away_table = home_away_tables[1]

    home_coach = soup.find(
        id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_LocalClubStats_lblHeadCoach").text
    away_coach = soup.find(
        id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_RoadClubStats_lblHeadCoach").text

    return get_table_markdown(home_table, home_team_name, home_coach), get_table_markdown(away_table, away_team_name, away_coach)


def get_table_markdown(table, name, coach):
    table_rows = table.find_all('tr')

    team_markdown = team_info_by_fs.get(name).full_md

    final_table = rh.get_reddit_table_head_and_cell_alignment([rc.NUMBER, team_markdown, rc.MINUTES, rc.POINTS, rc.FG2, rc.FG3, rc.FREE_TRHOWS,
                                                               rc.OFF_REBOUNDS, rc.DEF_REBOUNDS, rc.TOT_REBOUNDS, rc.ASSISTS, rc.STEALS, rc.TURNOVERS, rc.BLOCKS, rc.FOULS_COMMITED, rc.PIR])

    for row in table_rows[2: len(table_rows) - 1]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        # Removes the blocks against and fouls drawn columns
        cols.pop(16)
        cols.pop(14)

        cols_markdown = rh.build_table_delimitors(cols)
        final_table = rc.NEWLINE.join([final_table, cols_markdown])

    head_coach_markdown = rh.bold("Head Coach:") + coach
    final_table = rh.newline_join(
        [head_coach_markdown, rc.NEWLINE, final_table])

    return final_table


def get_final_score_markdown(home_team_name, home_team_score, away_team_name, away_team_score):
    final_table = rh.get_reddit_table_head_and_cell_alignment(
        ['TEAM', 'SCORE'])

    home_team_md = team_info_by_fs.get(home_team_name).full_md
    away_team_md = team_info_by_fs.get(away_team_name).full_md

    home_team_name_score = rh.build_table_delimitors(
        [home_team_md, home_team_score])
    away_team_name_score = rh.build_table_delimitors(
        [away_team_md, away_team_score])

    final_table = rh.newline_join(
        [final_table, home_team_name_score, away_team_name_score])

    return final_table


def get_game_information_markdown(soup):
    date_stadium_info_div = soup.find('div', class_='dates')

    date_info_cet = (date_stadium_info_div.find(
        'div', class_='date cet').text).replace('CET: ', '') + ' CET'
    stadium_info = date_stadium_info_div.find('span', class_='stadium').text
    attendance_info = soup.find(
        id='ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_lblAudience').text
    referees_info = soup.find(
        id='ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_lblReferees').text

    date_info_cet_markdown = rh.bold('Event Date:') + date_info_cet
    stadium_info_markdown = rh.bold('Stadium:') + stadium_info
    attendance_info_markdown = rh.bold('Attendance:') + attendance_info
    referees_info_markdown = rh.bold('Referees:') + referees_info

    return rh.newline_join([date_info_cet_markdown, rc.NEWLINE, stadium_info_markdown, rc.NEWLINE, attendance_info_markdown, rc.NEWLINE, referees_info_markdown])


def get_scores_table(soup, home_team, away_team):
    home_team_score = soup.find(
        class_="sg-score").find(class_="local").find(class_="score").text
    away_team_score = soup.find(
        class_="sg-score").find(class_="road").find(class_="score").text

    return get_final_score_markdown(home_team, home_team_score, away_team, away_team_score)


def is_page_ready(soup):
    # Checks if the top scores panel exists
    return not (soup.find('div', id='ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_gamescorestatic') is None)


def create_empty_thread(home_team, away_team, comp_round, comp_stage):
    home_team_parsed = team_info_by_fs.get(home_team).reddit
    away_team_parsed = team_info_by_fs.get(away_team).reddit

    title = 'Post-Match Thread: {home_team} - {away_team} [{comp} {comp_stage}, {comp_round}]'.format(
        comp=RedditGameThread.comp_info.comp_full_name, home_team=home_team_parsed, away_team=away_team_parsed, comp_round=comp_round, comp_stage=comp_stage)
    final_markdown = rc.REDDIT_THREAD_PLACEHOLDER_TEXT

    return submit_text_post(RedditGameThread.subreddit, title, final_markdown,
                            flair_text=RedditGameThread.comp_info.comp_small_name)


def handle_thread_update(home_team, away_team, submission, game_link):
    r = requests.get(game_link)

    soup = BeautifulSoup(r.text, 'html.parser')

    updated = False

    if is_page_ready(soup):
        final_game_information_markdown = get_game_information_markdown(soup)
        final_score_markdown = get_scores_table(soup, home_team, away_team)
        final_quarters_score_markdown = get_quarter_scores_markdown(
            soup, home_team, away_team)
        home_table_markdown, away_table_markdown = get_tables_markdown(
            soup, home_team, away_team)

        final_markdown = rh.newline_join([final_game_information_markdown, rc.REDDIT_HR, final_score_markdown, rc.REDDIT_HR,
                                          final_quarters_score_markdown, rc.REDDIT_HR, home_table_markdown, rc.NEWLINE, away_table_markdown])

        submission.edit(final_markdown)

        updated = True

    return submission, updated
