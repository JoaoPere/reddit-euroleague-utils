from reddit_utils import prepare_dot_env
from reddit_utils.team_structs import team_info_by_official
import reddit_utils.subreddit as sr
import reddit_utils.constants as rc
import reddit_utils.helpers as rh
from bs4 import BeautifulSoup
from collections import namedtuple
import requests
import praw
import sys
import os
import argparse


def get_quarter_scores_markdown(soup):
    quarter_table = soup.find(
        id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_PartialsStatsByQuarter_dgPartials")
    quarter_table_rows = quarter_table.find_all('tr')

    table_head_elements = [th.text.upper()
                           for th in quarter_table_rows[0].find_all('th')]
    final_table = rh.get_reddit_table_head_and_cell_alignment(
        table_head_elements, left_align_first=True)

    for row in quarter_table_rows[1:]:
        quarter_table_cols = row.find_all('td')
        quarter_table_cols = [ele.text.strip() for ele in quarter_table_cols]

        # Overrides the team name
        quarter_table_cols[0] = team_info_by_official.get(
            quarter_table_cols[0]).full_md

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

    team_markdown = team_info_by_official.get(name).full_md.upper()

    final_table = rh.get_reddit_table_head_and_cell_alignment([rc.NUMBER, team_markdown, rc.MINUTES, rc.POINTS, rc.FG2, rc.FG3, rc.FREE_TRHOWS,
                                                               rc.OFF_REBOUNDS, rc.DEF_REBOUNDS, rc.TOT_REBOUNDS, rc.ASSISTS, rc.STEALS, rc.TURNOVERS, rc.BLOCKS, rc.FOULS_COMMITED, rc.PIR])

    for row in table_rows[2: len(table_rows) - 1]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        # Removes the blocks against and fouls drawn columns
        cols.pop(16)
        cols.pop(14)

        cols_markdown = rh.build_table_delimitors(cols)
        final_table = rh.newline_join([final_table, cols_markdown])

    head_coach_markdown = rh.bold("Head Coach:") + coach
    final_table = rh.newline_join(
        [head_coach_markdown, rc.NEWLINE, final_table])

    return final_table


def get_final_score_markdown(home_team_name, home_team_score, away_team_name, away_team_score):
    final_table = rh.get_reddit_table_head_and_cell_alignment(
        ['TEAM', 'SCORE'], left_align_first=True)

    home_team_md = team_info_by_official.get(home_team_name).full_md
    away_team_md = team_info_by_official.get(away_team_name).full_md

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


def get_team_names_and_scores_table(soup):
    home_team_orig = soup.find(
        id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_LocalClubStats_lblTeamName").text
    away_team_orig = soup.find(
        id="ctl00_ctl00_ctl00_ctl00_maincontainer_maincontent_contentpane_boxscorepane_ctl00_RoadClubStats_lblTeamName").text

    home_team_name = team_info_by_official.get(home_team_orig).reddit
    away_team_name = team_info_by_official.get(away_team_orig).reddit

    home_team_score = soup.find(
        class_="sg-score").find(class_="local").find(class_="score").text
    away_team_score = soup.find(
        class_="sg-score").find(class_="road").find(class_="score").text

    return home_team_orig, home_team_name, away_team_orig, away_team_name, get_final_score_markdown(home_team_orig, home_team_score, away_team_orig, away_team_score)


def get_game_stage(soup):
    game_info_div = soup.find('div', class_='gc-title')
    game_info_spans = game_info_div.find_all('span')

    game_info_spans = list(map(lambda gi: gi.text.strip(), game_info_spans))

    comp_stage = game_info_spans[1]
    comp_round = game_info_spans[2]

    return comp_stage, comp_round


def get_competition_info(competition):
    ArgsParseTuple = namedtuple(
        'ArgsParseTuple', 'game_url comp_full_name')
    args_dict = dict()

    args_dict['EL'] = ArgsParseTuple(
        'https://www.euroleague.net/main/results/showgame?gamecode={}&seasoncode=E2020', 'EuroLeague')
    args_dict['EC'] = ArgsParseTuple(
        'https://www.eurocupbasketball.com/eurocup/games/results/showgame?gamecode={}&seasoncode=U2020', 'EuroCup')

    return args_dict.get(competition)


def build_thread_title_and_markdown(soup, competition: str):
    final_game_information_markdown = get_game_information_markdown(soup)
    home_team_orig, home_team_name, away_team_orig, away_team_name, final_score_markdown = get_team_names_and_scores_table(
        soup)
    final_quarters_score_markdown = get_quarter_scores_markdown(soup)
    home_table_markdown, away_table_markdown = get_tables_markdown(soup,
                                                                   home_team_orig, away_team_orig)
    comp_stage, comp_round = get_game_stage(soup)

    final_markdown = rh.newline_join([final_game_information_markdown, rc.REDDIT_HR, final_score_markdown, rc.REDDIT_HR,
                                      final_quarters_score_markdown, rc.REDDIT_HR, home_table_markdown, rc.NEWLINE, away_table_markdown])

    final_title = 'Post-Match Thread: {home_team} - {away_team} [{comp} {comp_stage}, {comp_round}]'.format(
        comp=competition, home_team=home_team_name, away_team=away_team_name, comp_round=comp_round, comp_stage=comp_stage)

    return final_title, final_markdown


def main():
    parser = argparse.ArgumentParser(description='Post game thread creator')
    parser.add_argument('competition', metavar='C',
                        type=str, choices=['EL', 'EC'])
    parser.add_argument('gamecode', metavar='G', type=int)
    args = parser.parse_args()
    competition_info = get_competition_info(args.competition)

    r = requests.get(competition_info.game_url.format(
        args.gamecode))
    soup = BeautifulSoup(r.text, 'html.parser')

    title, markdown = build_thread_title_and_markdown(
        soup, competition_info.comp_full_name)

    subreddit = sr.get_subreddit()
    sr.submit_text_post(subreddit, title, markdown,
                        flair_text=args.competition)


if __name__ == '__main__':
    main()
