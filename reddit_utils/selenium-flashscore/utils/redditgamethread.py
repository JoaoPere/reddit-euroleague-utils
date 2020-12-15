from .enumstates import ThreadState, GameState
from .redditthread import create_empty_thread, handle_thread_update
from reddit_utils.subreddit import get_subreddit


class RedditGameThread():
    comp_info = None
    subreddit = get_subreddit()

    def __init__(self, home_team, away_team, comp_round=None, comp_stage=None, game_state=GameState.UNFINISHED, thread_state=ThreadState.UNPUBLISHED, game_link=None, reddit_submission=None):
        self.home_team = home_team
        self.away_team = away_team

        self.comp_round = comp_round
        self.comp_stage = comp_stage

        self.game_state = game_state
        self.thread_state = thread_state

        self.game_link = game_link
        self.reddit_submission = reddit_submission

    def __str__(self):
        str_list = list()
        str_list.append('Matchup: {} vs {}'.format(
            self.home_team, self.away_team))
        str_list.append(
            'State: {} / {}'.format(self.thread_state, self.game_state))
        str_list.append('Game Link: {}'.format(self.game_link))
        str_list.append('Reddit Submission: {}'.format(
            'https://old.reddit.com/r/Euroleague/comments/' + str(self.reddit_submission)))
        return '\n'.join(str_list)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, RedditGameThread):
            return self.home_team == other.home_team and self.away_team == other.away_team
        return False

    @classmethod
    def set_competition_info(cls, comp_info):
        cls.comp_info = comp_info

    @property
    def home_team(self):
        return self._home_team

    @home_team.setter
    def home_team(self, value):
        self._home_team = value

    @property
    def away_team(self):
        return self._away_team

    @away_team.setter
    def away_team(self, value):
        self._away_team = value

    @property
    def comp_round(self):
        return self._comp_round

    @comp_round.setter
    def comp_round(self, value):
        self._comp_round = value

    @property
    def comp_stage(self):
        return self._comp_stage

    @comp_stage.setter
    def comp_stage(self, value):
        self._comp_stage = value

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        if value not in GameState:
            raise ValueError('Invalid game state')

        self._game_state = value

    @property
    def thread_state(self):
        return self._thread_state

    @thread_state.setter
    def thread_state(self, value):
        if value not in ThreadState:
            raise ValueError('Invalid thread state')

        self._thread_state = value

    @property
    def game_link(self):
        return self._game_link

    @game_link.setter
    def game_link(self, value):
        self._game_link = value

    @property
    def reddit_submission(self):
        return self._reddit_submission

    @reddit_submission.setter
    def reddit_submission(self, value):
        self._reddit_submission = value

    # Improve error handling
    def publish_thread(self):
        self.thread_state = ThreadState.PUBLISHING

        self.reddit_submission = create_empty_thread(
            self.home_team, self.away_team, self.comp_round, self.comp_stage)

        if self.reddit_submission is not None:
            self.thread_state = ThreadState.PUBLISHED

    # Improve error handling
    def update_thread(self):
        if self.reddit_submission is None:
            raise ValueError('Reddit Thread should not be null')

        self.reddit_submission, updated = handle_thread_update(
            self.home_team, self.away_team, self.reddit_submission, self.game_link)

        if updated:
            self._thread_state = ThreadState.COMPLETED
