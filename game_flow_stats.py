from datetime import datetime
from itertools import groupby
import csv

class Action(object):

    @classmethod
    def fromstring(cls, fields):
        return cls(*fields.strip('\n').split(','))

    def __init__(self, fid=None, year=None, day=None, wteam=None, lteam=None, game_sec_elapsed=None,
                       team=None, event=None, wscore=None, lscore=None):
        self.game_sec_elapsed = int(game_sec_elapsed)
        self.wteam = wteam
        self.lteam = lteam
        self.team = team
        self.event = event
        self.wscore = int(wscore)
        self.lscore = int(lscore)
        self.season = year
        self.day = day



class GameStats(object):

    def __init__(self, season=None, day=None, wteam=None, lteam=None):
        self.season = season
        self.day = day
        self.wteam = wteam
        self.lteam = lteam
        self.wteam_longest_streak = 0
        self.lteam_longest_streak = 0
        self.wteam_longest_streak_sec = 0
        self.lteam_longest_streak_sec = 0
        self.wteam_breakaway_pts = 0
        self.lteam_breakaway_pts = 0
        self.wteam_pos_sec = 0
        self.lteam_pos_sec = 0
        self.wteam_avg_time_to_score = 0.0
        self.lteam_avg_time_to_score = 0.0

def collect_actions_by_game(flow_records):
    games = []
    for game, flow_records in groupby(flow_records, key=lambda x: '|'.join(x.strip('\r\n').split(',')[1:5])):
        games.append([Action.fromstring(record) for record in flow_records])
    return games


def game_stats(game):
    print game[0]
    game_stats = GameStats(season=game[0].season, day=game[0].day, wteam=game[0].wteam, lteam=game[0].lteam)
    prev_score_team = None
    streak_begin_time = None
    streak = 0
    for action in game:
        if action.event.startswith('make'): #streak calculations
            cur_score_team = action.team
            if prev_score_team is None:
                prev_score_team = cur_score_team
            if streak_begin_time is None:
                streak_begin_time = action.game_sec_elapsed
            if cur_score_team == prev_score_team:
                streak += int(action.event[4:])
                streak_sec = action.game_sec_elapsed - streak_begin_time
                if cur_score_team == game_stats.wteam:
                    game_stats.wteam_longest_streak = max(game_stats.wteam_longest_streak, streak)
                    game_stats.wteam_longest_streak_sec = max(game_stats.wteam_longest_streak_sec, streak_sec)
                else:
                    game_stats.lteam_longest_streak = max(game_stats.lteam_longest_streak, streak)
                    game_stats.lteam_longest_streak_sec = max(game_stats.lteam_longest_streak_sec, streak_sec)
            else:
                streak = 0 + int(action.event[4:])
                streak_begin_time = action.game_sec_elapsed
            prev_score_team = cur_score_team #</streak calculations>
    return game_stats

if __name__ == '__main__':
    games = collect_actions_by_game(open('game_flow_details.csv', 'rb').readlines()[1:]) #trim flow id
    stats = game_stats(games)