from reddit_utils.team_structs import team_info_by_official
import reddit_utils.helpers as rh
from bs4 import BeautifulSoup
import requests
import sys
import argparse


def get_standings_table():
    r = requests.get('https://www.euroleague.net/main/standings')

    soup = BeautifulSoup(r.text, 'html.parser')

    final_table = rh.get_reddit_table_head_and_cell_alignment(
        ['#', '', 'W', 'L', '+/-'])

    # Returns only the standings table
    standings_table = soup.find_all("table")

    table_rows = standings_table[0].find_all('tr')

    for idx, row in enumerate(table_rows[1:]):
        cols = row.find_all('td')

        team_ahref = cols[0].find('a').text

        # Strips all the leading and trailing white space, removes the digits and shifts the string 2 positions to remove the '. ' substring
        team_name = ''.join(
            [i for i in team_ahref.strip() if not i.isdigit()])[2:]

        team_markdown = team_info_by_official.get(team_name).full_md

        position = str(idx + 1)
        wins = cols[1].text.strip()
        losses = cols[2].text.strip()
        plus_minus = cols[5].text.strip()

        plus_minus = '+' + \
            plus_minus if plus_minus[0].isdigit() else plus_minus

        cols_markdown = rh.build_table_delimitors(
            [position, team_markdown, wins, losses, plus_minus])

        final_table = rh.newline_join([final_table, cols_markdown])

    return final_table


def main():
    print(get_standings_table())


if __name__ == '__main__':
    main()
