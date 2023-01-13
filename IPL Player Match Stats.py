import pandas as pd
from dateutil.parser import parse

class MatchStats:
    def __init__(self):
        self.matches = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL_Matches_2022.csv')
        self.deliveries = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL_Ball_by_Ball_2022.csv')

    def player_career(self, player):
        return self.deliveries[self.deliveries['batsman'] == player]

    def best_match_id(self, player):
        top_score = self.player_career(player)[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum().sort_values(by='batsman_runs', ascending=False)[:1]
        return top_score.index[0][0]

    def player_best_match(self, player):
        return self.matches[self.matches['id'] == self.best_match_id(player)].iloc[0]

    def best_match_deliveries(self, player):
        match_deliveries = self.deliveries[self.deliveries['id'] == self.best_match_id(player)]
        return match_deliveries[match_deliveries['batsman'] == player]

    def city(self, best_match):
        return best_match['city']

    def season(self, best_match):
        return parse( best_match['date'], dayfirst=True ).year

    def match_date(self, best_match):
        return best_match['date']

    def runs_scored(self, match_deliveries):
        return int (match_deliveries[['batsman', 'batsman_runs']].groupby('batsman').sum()['batsman_runs'])

    def balls_faced(self, match_deliveries):
        return int( match_deliveries[match_deliveries['extra_runs'] == 0][['batsman', 'ball']].groupby('batsman').count()['ball'])

    def strike_rate(self, match_deliveries):
        return round (( self.runs_scored(match_deliveries) / self.balls_faced(match_deliveries) ) * 100, ndigits=2)

    def sixes_scored(self, match_deliveries):
        return int (match_deliveries[['batsman', 'batsman_runs']][match_deliveries['batsman_runs'] == 6].groupby('batsman').count()['batsman_runs'])

    def fours_scored(self, match_deliveries):
        return int (match_deliveries[['batsman', 'batsman_runs']][match_deliveries['batsman_runs'] == 4].groupby('batsman').count()['batsman_runs'])

    def player_match_stats(self, players):
        stats = []

        for player in players:
            best_match = self.player_best_match(player)
            match_deliveries = self.best_match_deliveries(player)

            row = [self.runs_scored(match_deliveries), self.balls_faced(match_deliveries), self.strike_rate(match_deliveries), self.fours_scored(match_deliveries), self.sixes_scored(match_deliveries), self.city(best_match), self.season(best_match)]
            stats.append(row)

        columns = ['Runs', 'BF', 'SR', '4s', '6s', 'City', 'Season']
        return print( pd.DataFrame(stats, index=[players], columns=columns).sort_values(by='Runs', ascending=False) )


# Player Summary Statistics 
# players = ['V Kohli', 'RR Pant', 'AB de Villiers', 'CH Gayle', 'DA Warner', 'BB McCullum', 'KL Rahul']
players = ['V Kohli', 'KL Rahul', 'JC Buttler', 'Q de Kock', 'F du Plessis', 'DA Miller']

stats = MatchStats()
stats.player_match_stats(players)