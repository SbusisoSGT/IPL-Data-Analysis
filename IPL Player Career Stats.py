import pandas as pd

matches = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Matches 2008-2020.csv')
deliveries = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL Ball-by-Ball 2008-2020.csv')


def player_career(player):
    return deliveries[deliveries['batsman'] == player]

def innings_runs(career):
    return career[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum(numeric_only=True).sort_values(by='batsman_runs' ,ascending=False)

def matches_played(career):
    return len(career['id'].unique())

def runs_scored(career):
    return int(career[['batsman', 'batsman_runs']].groupby('batsman').sum()['batsman_runs'])

def balls_faced(career):
    return int( career[career['extra_runs'] == 0][['batsman', 'ball']].groupby('batsman').count()['ball'])

def centuries_scored(career):
    return int (innings_runs(career)[innings_runs(career)['batsman_runs'] >= 100].count())

def fifties_scored(career):
    above_fifties = innings_runs(career)[innings_runs(career)['batsman_runs'] >= 50]
    return int (above_fifties[above_fifties['batsman_runs'] < 100].count() )

def sixes_scored(career):
    return int (career[['batsman', 'batsman_runs']][career['batsman_runs'] == 6].groupby('batsman').count()['batsman_runs'])

def fours_scored(career):
    return int (career[['batsman', 'batsman_runs']][career['batsman_runs'] == 4].groupby('batsman').count()['batsman_runs'])

def highscore(career):
    return int(innings_runs(career)[:1]['batsman_runs'])

def average(career):
    return round (float (career[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum().groupby('batsman').mean()['batsman_runs']), ndigits=2)

def strike_rate(career):
    return round (( runs_scored(career) / balls_faced(career) ) * 100, ndigits=2)


def player_stats(players):
    stats = []

    for player in players:
        career = player_career(player)
        row = [matches_played(career), runs_scored(career), balls_faced(career), average(career), strike_rate(career), highscore(career), centuries_scored(career), fifties_scored(career), fours_scored(career), sixes_scored(career)]
        stats.append(row)

    columns = ['Mat', 'Runs', 'BF', 'Avg', 'SR', 'HS', '100', '50', '4s', '6s']
    return pd.DataFrame(stats, index=[players], columns=columns)  


# Player Summary Statistics 
players = ['V Kohli', 'CH Gayle', 'DA Warner', 'BB McCullum', 'KL Rahul', 'AB de Villiers']

print(player_stats(players))