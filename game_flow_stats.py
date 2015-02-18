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

    def __init__(self, season=None, day=None, team=None):
        self.season = season
        self.day = day
        self.team = team
        self.longest_streak = 0
        self.longest_streak_sec = 0
        self.breakaway_pts = 0
        self.pos_sec = 0
        self.sec_between_scores = [] #take average at the end. avg_sec_between_scores
        self.pt_diffs_from_opp = [] #take average at the end. avg_pt_diff_from_opp
        self.recent_event_sec = 0
        self.recent_score_event_sec = 0


        #make into 2 relations. year wteam, year lteam. each relation half the original width. Union and then agg in
        # one pass.


def collect_actions_by_game(flow_records):
    games = []
    for game, flow_records in groupby(flow_records, key=lambda x: '|'.join(x.strip('\r\n').split(',')[1:5])):
        games.append([Action.fromstring(record) for record in flow_records])
    return games


def game_stats(game):
    w_game_stats = GameStats(season=game[0].season, day=game[0].day, team=game[0].wteam)
    l_game_stats = GameStats(season=game[0].season, day=game[0].day, team=game[0].lteam)
    prev_score_team = None
    streak_begin_time = None
    streak = 0
    for action in game:
        cur_score_team = action.team
        if cur_score_team == w_game_stats.team: #breakaway points
            w_game_stats.recent_event_sec = action.game_sec_elapsed
            if action.event.startswith('make'):
                if action.game_sec_elapsed - l_game_stats.recent_event_sec <= 4:
                    w_game_stats.breakaway_pts += int(action.event[4:])
        else:
            l_game_stats.recent_event_sec = action.game_sec_elapsed
            if action.event.startswith('make'):
                if action.game_sec_elapsed - w_game_stats.recent_event_sec <= 4:
                    l_game_stats.breakaway_pts += int(action.event[4:]) #</breakaway points>

        if cur_score_team == w_game_stats.team:
            w_game_stats.pt_diffs_from_opp.append(action.wscore - action.lscore)
        else:
            l_game_stats.pt_diffs_from_opp.append(action.lscore - action.wscore)

        if cur_score_team == w_game_stats.team: #pos_sec
            w_game_stats.recent_event_sec = action.game_sec_elapsed
            if action.event.startswith('make') \
                or action.event.startswith('miss') \
                or action.event.startswith('offreb') \
                or action.event.startswith('tover'):
                w_game_stats.pos_sec += (action.game_sec_elapsed - l_game_stats.recent_event_sec)
        else:
            l_game_stats.recent_event_sec = action.game_sec_elapsed
            if action.event.startswith('make') \
                or action.event.startswith('miss') \
                or action.event.startswith('offreb') \
                or action.event.startswith('tover'):
                l_game_stats.pos_sec += (action.game_sec_elapsed - w_game_stats.recent_event_sec) #</pos_sec>

        if cur_score_team == w_game_stats.team: #seconds between scores
            w_game_stats.sec_between_scores.append(action.game_sec_elapsed - w_game_stats.recent_score_event_sec)
            w_game_stats.recent_score_event_sec = action.game_sec_elapsed
        else:
            l_game_stats.sec_between_scores.append(action.game_sec_elapsed - l_game_stats.recent_score_event_sec)
            l_game_stats.recent_score_event_sec = action.game_sec_elapsed #</seconds between scores>

        if action.event.startswith('make'): #streak calculations

            if prev_score_team is None:
                prev_score_team = cur_score_team
            if streak_begin_time is None:
                streak_begin_time = action.game_sec_elapsed
            if cur_score_team == prev_score_team:
                streak += int(action.event[4:])
                streak_sec = action.game_sec_elapsed - streak_begin_time
                if cur_score_team == w_game_stats.team:
                    w_game_stats.longest_streak = max(w_game_stats.longest_streak, streak)
                    w_game_stats.longest_streak_sec = max(w_game_stats.longest_streak_sec, streak_sec)
                else:
                    l_game_stats.longest_streak = max(l_game_stats.longest_streak, streak)
                    l_game_stats.longest_streak_sec = max(l_game_stats.longest_streak_sec, streak_sec)
            else:
                streak = 0 + int(action.event[4:])
                streak_begin_time = action.game_sec_elapsed
            prev_score_team = cur_score_team # </streak calculations>
    final_elapsed_sec = game[-1].game_sec_elapsed
    w_game_stats.pos_perc = float(w_game_stats.pos_sec) / final_elapsed_sec
    l_game_stats.pos_perc = float(l_game_stats.pos_sec) / final_elapsed_sec
    w_game_stats.avg_sec_between_scores = float(reduce(lambda x, y: x + y, w_game_stats.sec_between_scores, 0)) \
                                           / len(w_game_stats.sec_between_scores)
    l_game_stats.avg_sec_between_scores = float(reduce(lambda x, y: x + y, l_game_stats.sec_between_scores, 0)) \
                                           / len(l_game_stats.sec_between_scores)

    w_game_stats.avg_pt_diff_from_opp = float(reduce(lambda x, y: x + y, w_game_stats.pt_diffs_from_opp, 0)) \
                                           / len(w_game_stats.pt_diffs_from_opp)
    l_game_stats.avg_pt_diff_from_opp = float(reduce(lambda x, y: x + y, l_game_stats.pt_diffs_from_opp, 0)) \
                                           / len(l_game_stats.pt_diffs_from_opp)
    return [w_game_stats, l_game_stats]

if __name__ == '__main__':
    games = collect_actions_by_game(open('game_flow_details.csv', 'rb').readlines()[1:]) #trim flow id
    stats = [game_stats(game) for game in games]