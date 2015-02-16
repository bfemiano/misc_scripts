
import unittest
from game_flow_stats import game_stats, Action

class GameFlowStatsTest(unittest.TestCase):

    def test_streak(self):
        game = [Action(year=2010, day=20, wteam=1, lteam=2, team=1, event='make1', game_sec_elapsed=5, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=13, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=17, wscore=5, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='turn', game_sec_elapsed=22, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='steal', game_sec_elapsed=28, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make3', game_sec_elapsed=33, wscore=3, lscore=0), #end team one scoring streak.
                Action(wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=35, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=40, wscore=3, lscore=0), #end team two scoring streak.
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=45, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=50, wscore=3, lscore=0), #smaller team1 streak, not the max.
                ]
        stats = game_stats(game)
        assert stats.wteam_longest_streak == 8
        assert stats.lteam_longest_streak == 5
        assert stats.wteam_longest_streak_sec == 28
        assert stats.lteam_longest_streak_sec == 5

    def test_longer_mid_flow_streak(self):

        game = [Action(year=2010, day=20, wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=1, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=5, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=13, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=17, wscore=5, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='turn', game_sec_elapsed=22, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='steal', game_sec_elapsed=28, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make3', game_sec_elapsed=34, wscore=3, lscore=0), #end team one scoring streak.
                Action(wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=35, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=40, wscore=3, lscore=0), #end team two scoring streak.
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=45, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=50, wscore=3, lscore=0), #smaller team1 streak, not the max.
                ]
        stats = game_stats(game)
        assert stats.wteam_longest_streak == 9
        assert stats.wteam_longest_streak_sec == 29


    def test_breakaway_pts(self):
        '''If a makeX for some team occurs within 4 seconds of the nearest opposing team event.'''
        pass #TODO: implement logic and test

    def test_pos_sec(self):
        '''For a given event, add the difference between the current event to the event prev against the team's
            pos seconds count. The total between teams should be at least 60 (or more if OT)'''
        pass #TODO: implement logic and test

    def test_avg_time_to_score(self):
        '''For each team, keep a list of scoring event differences between when the scoring event occurred, and when the most
        recent opposing team event occurred. '''
        pass #TODO: implement logic and test


if __name__ == '__main__':
    unittest.main()