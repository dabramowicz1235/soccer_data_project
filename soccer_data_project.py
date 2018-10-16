import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect(r"C:\Users\dabramowicz\Downloads\database.sqlite")

country = pd.read_sql_query('select * from Country;', conn)
league = pd.read_sql_query('select * from League;', conn)
match = pd.read_sql_query('select * from Match;', conn)
player = pd.read_sql_query('select * from Player;', conn)
player_attributes = pd.read_sql_query('select * from Player_Attributes;', conn)
team = pd.read_sql_query('select * from Team;', conn)
team_attributes = pd.read_sql_query('select * from Team_Attributes;', conn)
premier_league_id = 1729
print(player_attributes.columns)
premier_league_games = match[(match.league_id == premier_league_id)].reset_index()

premier_league_games = premier_league_games[['league_id', 'season', 'date', 'home_team_api_id', 'away_team_api_id', 'home_team_goal', 'away_team_goal', 'home_player_1', 'home_player_2', 'home_player_3', 'home_player_4', 'home_player_5', 'home_player_6', 'home_player_7', 'home_player_8', 'home_player_9', 'home_player_10', 'home_player_11', 'away_player_1','away_player_2', 'away_player_3', 'away_player_4', 'away_player_5', 'away_player_6', 'away_player_7', 'away_player_8', 'away_player_9', 'away_player_10', 'away_player_11']].reset_index()
#check relevant tables for nulls and remove accordingly
def drop_null_and_show(dataframe, show_cols = True):
    print(dataframe.isnull().any().any(), dataframe.shape)
    if show_cols == True:
        print(dataframe.isnull().sum(axis=0))
    if dataframe.isnull().any().any() == True:
        dataframe = dataframe.dropna()
    print(dataframe.isnull().any().any(), dataframe.shape)
drop_null_and_show(premier_league_games)
drop_null_and_show(player_attributes)

#now to clean up our data. This will add necessary columns and fill thsoe columns with each players' overall rating. It will NOT ACCOUNT FOR DATE!
for column in range(1,12):
    col_name = 'home_player_' + '{}'.format(column) + '_rating'
    premier_league_games[col_name] = 0
for column in range(1,12):
    col_name = 'away_player_' + '{}'.format(column) + '_rating'
    premier_league_games[col_name] = 0
print(premier_league_games.columns)
for match in range(len(premier_league_games)):
    for column in range(1,12):
        for team in ['home', 'away']:
            player_id = premier_league_games.loc[match, '{}'.format(team) + '_player_' + '{}'.format(column)]
            ratings = player_attributes.loc[player_attributes['player_api_id'] == player_id].reset_index()
            if ratings.empty:
                premier_league_games.loc[match, '{}'.format(team) + '_player_' + '{}'.format(column) + '_rating']= 0
            else:
                rating = ratings.iloc[0,5]
                premier_league_games.loc[match, '{}'.format(team) + '_player_' + '{}'.format(column) + '_rating'] = rating
premier_league_games.to_csv(r"C:\Users\dabramowicz\Documents\soccer_data_project\premier_league_games.csv")

plg = pd.read_csv(r"premier_league_games.csv")
