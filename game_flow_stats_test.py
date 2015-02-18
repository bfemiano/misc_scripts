
import unittest
from game_flow_stats import game_stats, Action

class GameFlowStatsTest(unittest.TestCase):

    def test_streak(self):
        '''Most consecutive points in seconds for wteam and lteam'''
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
        (w_stats, l_stats) = game_stats(game)
        assert w_stats.longest_streak == 8
        assert l_stats.longest_streak == 5
        assert w_stats.longest_streak_sec == 28
        assert l_stats.longest_streak_sec == 5

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
        (w_stats, l_stats) = game_stats(game)
        assert w_stats.longest_streak == 9
        assert w_stats.longest_streak_sec == 29

    def test_breakaway_pts(self):
        game = [Action(year=2010, day=20, wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=1, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=5, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make3', game_sec_elapsed=9, wscore=5, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='turn', game_sec_elapsed=22, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='steal', game_sec_elapsed=28, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make3', game_sec_elapsed=34, wscore=3, lscore=0), #end team one scoring streak.
                Action(wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=35, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=40, wscore=3, lscore=0), #end team two scoring streak.
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=45, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=50, wscore=3, lscore=0), #smaller team1 streak, not the max.
                ]
        (w_stats, l_stats) = game_stats(game)
        assert w_stats.breakaway_pts == 2
        assert l_stats.breakaway_pts == 4

    def test_pos_sec(self):
        '''For a given offensive event, take the difference between the offensive event and the previous event for the opposing team
            and count it towards the team's pos seconds count. An offensive event is considered: assist, makeX, missX, offreb, or tover.
            The total between teams should be at least 60 (or more if OT). Log possession time / minutes played in game. '''
        game = [Action(year=2010, day=20, wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=1, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=5, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=9, wscore=5, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=22, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='steal', game_sec_elapsed=28, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=34, wscore=3, lscore=0), #end team one scoring streak.
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=37, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=39, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=40, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=42, wscore=3, lscore=0), #end team two scoring streak.
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=45, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='tover', game_sec_elapsed=47, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=50, wscore=3, lscore=0), #smaller team1 streak, not the max.
                ]
        (w_stats, l_stats) = game_stats(game)
        assert w_stats.pos_sec == 27 #4 + 13 + 3 + 1 + 3 + 3
        assert l_stats.pos_sec == 23 #1+ 4 + 12 + 2 + 2
        assert w_stats.pos_perc == 0.54
        assert l_stats.pos_perc == 0.46


    def test_avg_time_to_score(self):
        '''For each team, keep a list of scoring event differences between when the scoring event occurred, and when the
        prev scoring event for that team occurred. Avg the list of time differences. '''
        game = [Action(year=2010, day=20, wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=1, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=5, wscore=1, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=9, wscore=5, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=22, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='steal', game_sec_elapsed=28, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=34, wscore=3, lscore=0), #end team one scoring streak.
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=37, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=39, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=40, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=42, wscore=3, lscore=0), #end team two scoring streak.
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=45, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=2, event='tover', game_sec_elapsed=47, wscore=3, lscore=0),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=50, wscore=3, lscore=0), #smaller team1 streak, not the max.
                ]
        (w_stats, l_stats) = game_stats(game)
        assert round(w_stats.avg_sec_between_scores) == round(8.33)
        assert round(l_stats.avg_sec_between_scores) == round(6.71)


    def test_avg_point_difference(self):
        '''For a given game, what were the average point differences between the two teams'''
        game = [Action(year=2010, day=20, wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=1, wscore=0, lscore=2),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=5, wscore=2, lscore=2),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=9, wscore=2, lscore=5),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=22, wscore=2, lscore=5),
                Action(wteam=1, lteam=2, team=2, event='steal', game_sec_elapsed=28, wscore=2, lscore=5),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=34, wscore=2, lscore=8),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=37, wscore=4, lscore=6),
                Action(wteam=1, lteam=2, team=2, event='make2', game_sec_elapsed=39, wscore=4, lscore=8),
                Action(wteam=1, lteam=2, team=1, event='tover', game_sec_elapsed=40, wscore=4, lscore=8),
                Action(wteam=1, lteam=2, team=2, event='make3', game_sec_elapsed=42, wscore=6, lscore=11),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=45, wscore=8, lscore=11),
                Action(wteam=1, lteam=2, team=2, event='tover', game_sec_elapsed=47, wscore=8, lscore=11),
                Action(wteam=1, lteam=2, team=1, event='make2', game_sec_elapsed=50, wscore=10, lscore=11)
                ]
        (w_stats, l_stats) = game_stats(game)
        assert round(w_stats.avg_pt_diff_from_opp) == round(-2.16)
        assert round(l_stats.avg_pt_diff_from_opp) == round(3.71)

if __name__ == '__main__':
    unittest.main()