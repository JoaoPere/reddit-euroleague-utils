from reddit_utils.constants import TABLE_DELIM, BOLD_MARKDOWN, NEWLINE, CELL_ALLIGNMENT, DOUBLE_NEWLINE


def build_table_delimitors(content: list):
    return TABLE_DELIM + TABLE_DELIM.join(content) + TABLE_DELIM


def build_table_alignment(length: int):
    return build_table_delimitors([CELL_ALLIGNMENT] * length)


def newline_join(content: list):
    return NEWLINE.join(content)


def double_newline_join(content: list):
    return DOUBLE_NEWLINE.join(content)


def get_reddit_table_head_and_cell_alignment(table_head: list):
    # Formatting table headings
    reddit_table_head = build_table_delimitors(table_head)

    # Reddit cell alignment
    reddit_cell_allignment = build_table_alignment(len(table_head))

    return newline_join([reddit_table_head, reddit_cell_allignment])


def bold(text: str):
    return BOLD_MARKDOWN + text + BOLD_MARKDOWN
