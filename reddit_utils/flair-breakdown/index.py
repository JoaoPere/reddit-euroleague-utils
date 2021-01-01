from itertools import repeat
import os
import sys
import argparse


def get_path_from_month_and_year(year: int, month: int):
    count_dir = os.path.join(os.getcwd(), 'counts')
    return os.path.join(os.path.join(count_dir, '{}_{}.txt'.format(year, month)))


def get_count_table_from_path(path: str):
    with open(path, encoding='utf8') as c:
        lines = c.readlines()
        count_table = lines[2:]

        count_table = [c.strip() for c in count_table]

        return count_table


def get_split_cells(table: str):
    return dict(cell.split(' | ') for cell in table)


def func_difference(active_cells, last_cells):
    team_name = active_cells[0]

    if team_name in last_cells.keys():
        diff = int(active_cells[1]) - int(last_cells[team_name])

        if diff == 0:
            return None
    else:
        diff = int(active_cells[1])

    return '{} | {}'.format(team_name, diff)


def func_difference_no_longer_used(last_cells, active_cells):
    team_name = last_cells[0]

    if team_name not in active_cells.keys():
        diff = -(int(last_cells[1]))
        return '{} | {}'.format(team_name, diff)


def func_sort(e: list):
    return int(e.split(' | ')[1])


def get_difference_list(active_table: str, last_table: str):
    active_cells = get_split_cells(active_table)
    last_cells = get_split_cells(last_table)

    difference = filter(lambda x: x is not None, map(
        func_difference, active_cells.items(), repeat(last_cells)))
    new_unused_flairs = filter(lambda x: x is not None, map(
        func_difference_no_longer_used, last_cells.items(), repeat(active_cells)))
    return sorted(list(difference) + list(new_unused_flairs), key=func_sort, reverse=True)


def pad_month(month: int):
    return str(month).zfill(2)


def get_markdown(diff_list):
    return '\n'.join(['Flair | Count', '---|---', *diff_list])


def get_counts(year: int, month: int):
    if month == 1:
        last_month = 12
        last_year = year-1
    else:
        last_month = month - 1
        last_year = year

    padded_month = pad_month(month)
    padded_last_month = pad_month(last_month)

    count_month_active_path = get_path_from_month_and_year(year, padded_month)
    count_month_last_path = get_path_from_month_and_year(
        last_year, padded_last_month)

    count_month_active = get_count_table_from_path(count_month_active_path)
    count_month_last = get_count_table_from_path(count_month_last_path)

    return count_month_active, count_month_last


def main():
    parser = argparse.ArgumentParser(
        description='Flair breakdown monthly table builder')
    time_group = parser.add_argument_group('time')
    time_group.add_argument('year', type=int, choices=[2020, 2021])
    time_group.add_argument('month', type=int, choices=range(1, 13))
    args = parser.parse_args()

    count_month_active, count_month_last = get_counts(
        args.year, args.month)
    difference_list = get_difference_list(count_month_active, count_month_last)
    markdown = get_markdown(difference_list)
    print(markdown)
    print()
    print('Amount of new flairs: {}'.format(
        sum(func_sort(d) for d in difference_list)))


if __name__ == '__main__':
    main()
