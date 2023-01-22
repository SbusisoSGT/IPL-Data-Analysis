import pandas as pd
from dateutil.parser import parse

class BowlerStats:
    def __init__(self, season=None):
        self.matches = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Matches 2008-2020.csv')
        self.deliveries = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Ball-by-Ball 2008-2020.csv')
        self.matches['season'] = pd.DatetimeIndex(self.matches['date'], dayfirst=True).year
        
        if(season != None):
            self.season = season
            matches_ids = self.matches[self.matches['season'] == season].reset_index()['id']
            matches_season = pd.DataFrame(matches_ids, columns=['id'])
            self.deliveries = self.deliveries.merge(matches_season, on='id')

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

    def average(self, career):
        return round ( self.runs_conceded(career) / self.wickets(career),  ndigits=1 )


    def economy(self, career):
        return round ( self.runs_conceded(career) / self.overs_faced(career),  ndigits=1 )

    def strike_rate(self, career):
        return round ( ((self.overs_faced(career) * 6) / self.wickets(career) ) , ndigits=1)

    def fivers(self, career):
        wickets = career[['id', 'is_wicket']].groupby('id').sum()
        return wickets[wickets['is_wicket'] == 5]['is_wicket'].count()

    def fourvers(self, career):
        wickets = career[['id', 'is_wicket']].groupby('id').sum()
        return wickets[wickets['is_wicket'] == 4]['is_wicket'].count()

    def top_ten_bowlers(self):
        bowlers = self.deliveries[['bowler', 'is_wicket']].groupby('bowler').sum().sort_values(by='is_wicket', ascending=False)[:10]
        return bowlers.index

    def player_career_stats(self, players=None, sortby=['Wkts', False]):
        stats = []

        players = self.top_ten_bowlers()

        for player in players:
            career = self.player_career(player)
            row = [self.matches_played(career), self.overs_faced(career), self.runs_conceded(career), self.wickets(career), self.best_bowling_figures(player), self.average(career),self.economy(career), self.strike_rate(career), self.fourvers(career), self.fivers(career)]
            
            stats.append(row)

        columns = ['Mat', 'Ov', 'Runs', 'Wkts', 'BBF', 'Avg', 'Econ', 'SR', '4w', '5w']
        return print (pd.DataFrame(stats, index=[players], columns=columns).sort_values(by=sortby[0], ascending=sortby[1]) )


# Player Summary Statistics 
stats = BowlerStats(season=2020)
stats.player_career_stats(sortby=['4w', False])