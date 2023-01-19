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

    def city(self, best_match):
        return best_match['city']

    def season(self, best_match):
        return parse( best_match['date'], dayfirst=True ).year

    def match_date(self, best_match):
        return best_match['date']

    def runs_conceded(self, deliveries):
        return int (deliveries[['bowler', 'total_runs']].groupby('bowler').sum()['total_runs'])

    def dots(self, deliveries):
        return deliveries['total_runs'][deliveries['total_runs'] == 0].count()

    def overs_faced(self, deliveries):
        return len(deliveries['over'].unique())

    def wickets(self, deliveries):
        return int (deliveries[['bowler', 'is_wicket']].groupby('bowler').sum()['is_wicket'])

    def best_bowling_figures(self, deliveries):
        figures = deliveries[['bowler', 'is_wicket', 'total_runs']].groupby('bowler').sum(numeric_only=True).sort_values(by=['is_wicket', 'total_runs'], ascending=[False, True]).iloc[0]
        return str(figures['is_wicket']) + '/' + str(figures['total_runs'])

    def economy(self, deliveries):
        return round ( self.runs_conceded(deliveries) / self.overs_faced(deliveries),  ndigits=1 )
    
    def strike_rate(self, deliveries):
        return round ( ((self.overs_faced(deliveries) * 6) / self.wickets(deliveries) ) , ndigits=1)

    def player_match_stats(self, players):
        stats = []

        for player in players:
            best_match = self.player_best_match(player)
            match_deliveries = self.best_match_deliveries(player)

            row = [self.overs_faced(match_deliveries), self.runs_conceded(match_deliveries), self.wickets(match_deliveries), self.best_bowling_figures(match_deliveries), self.dots(match_deliveries), self.economy(match_deliveries), self.strike_rate(match_deliveries), self.city(best_match), self.season(best_match)]
            stats.append(row)

        columns = ['Ov', 'Runs', 'Wkts', 'BBF', 'Dots', 'Econ', 'SR', 'City', 'Season']
        return print (pd.DataFrame(stats, index=[players], columns=columns).sort_values(by=['Wkts', 'Runs'], ascending=[False, True]) )


# Player Summary Statistics 
#players = ['JJ Bumrah', 'Rashid Khan', 'JR Hazlewood', 'K Rabada', 'PJ Cummins', 'YS Chahal', 'A Nortje', 'AD Russell'] 
players = ['AS Joseph', 'SL Malinga', 'DW Steyn', 'R Ashwin', 'Rashid Khan']

stats = BowlerStats()
stats.player_match_stats(players)