import pandas as pd
from dateutil.parser import parse

matches = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL_Matches_2022.csv')
deliveries = pd.read_csv('C:/Users/Princess Muthimunye/OneDrive/Documents/Machine Learning Datasets/IPL Dataset and Code/IPL_Ball_by_Ball_2022.csv')

def player_career(player):
    return deliveries[deliveries['batsman'] == player]

def player_best_match(player):
    top_score = player_career(player)[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum().sort_values(by='batsman_runs', ascending=False)[:1]
    id = top_score.index[0][0]
    return matches[matches['id'] == id].iloc[0]

def best_match_deliveries(player):
    top_score = player_career(player)[['id', 'batsman', 'batsman_runs']].groupby(['id', 'batsman']).sum().sort_values(by='batsman_runs', ascending=False)[:1]
    id = top_score.index[0][0]
    match_deliveries = deliveries[deliveries['id'] == id]
    return match_deliveries[match_deliveries['batsman'] == player]

def city(best_match):
    return best_match['venue']

def season(best_match):
    return parse( best_match['date'], dayfirst=True ).year

def match_date(best_match):
    return best_match['date']

def runs_scored(deliveries):
    return int (deliveries[['batsman', 'batsman_runs']].groupby('batsman').sum()['batsman_runs'])

def balls_faced(deliveries):
    return int( deliveries[deliveries['extra_runs'] == 0][['batsman', 'ball']].groupby('batsman').count()['ball'])

def strike_rate(deliveries):
    return round (( runs_scored(deliveries) / balls_faced(deliveries) ) * 100, ndigits=2)

def sixes_scored(deliveries):
    return int (deliveries[['batsman', 'batsman_runs']][deliveries['batsman_runs'] == 6].groupby('batsman').count()['batsman_runs'])

def fours_scored(deliveries):
    return int (deliveries[['batsman', 'batsman_runs']][deliveries['batsman_runs'] == 4].groupby('batsman').count()['batsman_runs'])

def player_match_stats(players):
    stats = []

    for player in players:
        best_match = player_best_match(player)
        match_deliveries = best_match_deliveries(player)

        row = [runs_scored(match_deliveries), balls_faced(match_deliveries), strike_rate(match_deliveries), fours_scored(match_deliveries), sixes_scored(match_deliveries), city(best_match), season(best_match)]
        stats.append(row)

    columns = ['Runs', 'BF', 'SR', '4s', '6s', 'Venue', 'Season']
    return pd.DataFrame(stats, index=[players], columns=columns).sort_values(by='Runs', ascending=False)


# Player Summary Statistics 
players = ['V Kohli', 'KL Rahul', 'JC Buttler', 'Q de Kock', 'F du Plessis', 'DA Miller'] #'RR Pant', 'AB de Villiers', 'CH Gayle', 'DA Warner', 'BB McCullum', 'KL Rahul',]

print(player_match_stats(players))