from enum import Enum

class ThreadState(Enum):
    UNPUBLISHED = 0,
    PUBLISHING = 1
    PUBLISHED = 2,
    COMPLETED = 3


class GameState(Enum):
    UNFINISHED = 0,
    FINISHED = 1
