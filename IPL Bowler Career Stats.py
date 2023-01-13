import pandas as pd
from dateutil.parser import parse

class BowlerStats:
    def __init__(self):
        self.matches = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Matches 2008-2020.csv')
        self.deliveries = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Ball-by-Ball 2008-2020.csv')

    def player_career(self, player):
        return self.deliveries[self.deliveries['bowler'] == player]
    
    def best_match_id(self, player):
        bowling_figures = self.player_career(player)[['id', 'bowler', 'is_wicket', 'total_runs']].groupby(['id', 'bowler']).sum(numeric_only=True).sort_values(by=['is_wicket', 'total_runs'], ascending=[False, True])[:1]
        return bowling_figures.index[0][0]

    def player_best_match(self, player):
        return self.matches[self.matches['id'] == self.best_match_id(player)].iloc[0]

    def best_match_deliveries(self, player):
        match_deliveries = self.deliveries[self.deliveries['id'] == self.best_match_id(player)]
        return match_deliveries[match_deliveries['bowler'] == player]

    def best_bowling_figures(self, player):
        deliveries = self.best_match_deliveries(player)
        figures = deliveries[['bowler', 'is_wicket', 'total_runs']].groupby('bowler').sum(numeric_only=True).sort_values(by=['is_wicket', 'total_runs'], ascending=[False, True]).iloc[0]
        return str(figures['is_wicket']) + '/' + str(figures['total_runs'])

    def matches_played(self, career):
        return len(career['id'].unique())

    def runs_conceded(self, career):
        return int (career[['bowler', 'total_runs']].groupby('bowler').sum()['total_runs'])

    def overs_faced(self, career):
        return round (len(career['over']) / 6)

    def wickets(self, career):
        return int (career[['bowler', 'is_wicket']].groupby('bowler').sum()['is_wicket'])

    def economy(self, career):
        return round ( self.runs_conceded(career) / self.overs_faced(career),  ndigits=1 )

    def fivers(self, career):
        wickets = career[['id', 'is_wicket']].groupby('id').sum()
        return wickets[wickets['is_wicket'] == 5]['is_wicket'].count()

    def fourvers(self, career):
        wickets = career[['id', 'is_wicket']].groupby('id').sum()
        return wickets[wickets['is_wicket'] == 4]['is_wicket'].count()

    def player_career_stats(self, players):
        stats = []

        for player in players:
            career = self.player_career(player)
            row = [self.matches_played(career), self.overs_faced(career), self.runs_conceded(career), self.wickets(career), self.best_bowling_figures(player), self.economy(career), self.fourvers(career), self.fivers(career)]
            
            stats.append(row)

        columns = ['Mat', 'Ov', 'Runs', 'Wkts', 'BBF', 'Econ', '4w', '5w']
        return print (pd.DataFrame(stats, index=[players], columns=columns).sort_values(by='Wkts', ascending=False) )


# Player Summary Statistics 
players = ['SL Malinga', 'DJ Bravo', 'R Ashwin', 'K Rabada', 'B Kumar', 'JJ Bumrah', 'YS Chahal', 'DW Steyn', 'CH Morris',]

stats = BowlerStats()
stats.player_career_stats(players)