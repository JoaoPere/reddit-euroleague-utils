from reddit_utils.constants import TABLE_DELIM, BOLD_MARKDOWN, NEWLINE, LEFT_CELL_ALIGNMENT, CENTER_CELL_ALIGNMENT, DOUBLE_NEWLINE


def build_table_delimitors(content: list):
    return TABLE_DELIM + TABLE_DELIM.join(content) + TABLE_DELIM


def get_reddit_table_head_and_cell_alignment(table_head: list, left_align_first: bool = False):
    def build_table_alignment(length: int, left_align_first: bool):
        if left_align_first:
            return build_table_delimitors([LEFT_CELL_ALIGNMENT] +
                                          [CENTER_CELL_ALIGNMENT] * (length - 1))
        else:
            return build_table_delimitors([CENTER_CELL_ALIGNMENT] * length)

    # Formatting table headings
    reddit_table_head = build_table_delimitors(table_head)

    # Reddit cell alignment
    reddit_cell_allignment = build_table_alignment(
        len(table_head), left_align_first)

    return newline_join([reddit_table_head, reddit_cell_allignment])


def newline_join(content: list):
    return NEWLINE.join(content)


def double_newline_join(content: list):
    return DOUBLE_NEWLINE.join(content)


def bold(text: str):
    return BOLD_MARKDOWN + text + BOLD_MARKDOWN + ' '
