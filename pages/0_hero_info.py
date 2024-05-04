import streamlit as st
import pandas as pd
import map_hero_choices as mh
import stat_util as su

# set up dfs
game_history_df = pd.read_csv('data/game_history.csv')
hero_stats_df = pd.read_csv('data/hero_stats.csv')
map_stats_df = pd.read_csv('data/map_stats.csv')

# const options for entry creation
maps = mh.MAPS.keys()
heroes = mh.HEROES.keys()
outcomes = mh.OUTCOMES
modes = mh.MODES

st.title('Hero Info')

# mode filter 
mode_selection = st.selectbox('Modes', ['All Games', 'Competitive', 'Unranked'])
if mode_selection != 'All Games':
    games = game_history_df[game_history_df['mode'] == mode_selection]
else:
    games = game_history_df

# role filter
role_selection = st.selectbox('Roles', ['All Roles', 'Tank', 'DPS', 'Support'])
if role_selection != 'All Roles':
    role_heroes = hero_stats_df[hero_stats_df['role'] == role_selection]
    role_heroes
else:
    #display all heroes
    pass