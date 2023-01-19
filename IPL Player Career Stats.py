import pandas as pd

class CareerStats:
    def __init__(self, season=None):
        self.matches = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Matches 2008-2020.csv')
        self.matches['season'] = pd.DatetimeIndex(self.matches['date'], dayfirst=True).year
        self.deliveries = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Ball-by-Ball 2008-2020.csv')

        if(season != None):
            self.season = season
            matches_ids = self.matches[self.matches['season'] == season].reset_index()['id']
            matches_season = pd.DataFrame(matches_ids, columns=['id'])
            self.deliveries = self.deliveries.merge(matches_season, on='id')

    def player_career(self, player):
        return self.deliveries[self.deliveries['batsman'] == player]

    def innings_runs(self, career):
        return career[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum(numeric_only=True).sort_values(by='batsman_runs' ,ascending=False)

    def matches_played(self, career):
        return len(career['id'].unique())

    def runs_scored(self, career):
        return int( career[['batsman', 'batsman_runs']].groupby('batsman').sum()['batsman_runs'] )

    def balls_faced(self, career):
        return int( career[career['extra_runs'] == 0][['batsman', 'ball']].groupby('batsman').count()['ball'])

    def highscore_dismissed(self, career):
        highscore = career[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum(numeric_only=True).sort_values(by='batsman_runs' ,ascending=False)[:1]

    def centuries_scored(self, career):
        return int (self.innings_runs(career)[self.innings_runs(career)['batsman_runs'] >= 100].count())

    def fifties_scored(self, career):
        above_fifties = self.innings_runs(career)[self.innings_runs(career)['batsman_runs'] >= 50]
        return int (above_fifties[above_fifties['batsman_runs'] < 100].count() )

    def sixes_scored(self, career):
        return int (career[['batsman', 'batsman_runs']][career['batsman_runs'] == 6].groupby('batsman').count()['batsman_runs'])

    def fours_scored(self, career):
        return int (career[['batsman', 'batsman_runs']][career['batsman_runs'] == 4].groupby('batsman').count()['batsman_runs'])

    def highscore(self, career):
        return int(self.innings_runs(career)[:1]['batsman_runs'])

    def average(self, career):
        return round (float (career[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum().groupby('batsman').mean()['batsman_runs']), ndigits=2)

    def strike_rate(self, career):
        return round (( self.runs_scored(career) / self.balls_faced(career) ) * 100, ndigits=2)

    def top_ten_batsmen(self):
        batsmen = self.deliveries[['batsman', 'batsman_runs']].groupby('batsman').sum().sort_values(by='batsman_runs', ascending=False)[:10]
        return batsmen.index

    def player_stats(self, players=None):
        stats = []

        if (players == None):
            players = self.top_ten_batsmen()

        for player in players:
            career = self.player_career(player)
            if(career.empty):
                continue
            else:
                row = [self.matches_played(career), self.runs_scored(career), self.balls_faced(career), self.average(career), self.strike_rate(career), self.highscore(career), self.centuries_scored(career), self.fifties_scored(career), self.fours_scored(career), self.sixes_scored(career)]
                stats.append(row)

        columns = ['Mat', 'Runs', 'BF', 'Avg', 'SR', 'HS', '100', '50', '4s', '6s']
        return print( pd.DataFrame(stats, index=[players], columns=columns).sort_values(by='Runs', ascending=False) )


# Player Summary Statistics 
players = ['V Kohli', 'CH Gayle', 'DA Warner', 'BB McCullum', 'KL Rahul', 'AB de Villiers', 'S Dhawan']

stats = CareerStats(season=2020)
stats.player_stats(players=None)