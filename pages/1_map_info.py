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

st.title('Map Info')

# mode filter 
mode_selection = st.selectbox('Modes', ['All Games', 'Competitive', 'Unranked'])
if mode_selection != 'All Games':
    games = game_history_df[game_history_df['mode'] == mode_selection]
else:
    games = game_history_df

# objective filter
objective_selection = st.selectbox('Objectives', ['All Objectives', 'Control', 'Escort', 'Flashpoint', 'Hybrid', 'Push'])
if objective_selection != 'All Objectives':
    objective_maps = map_stats_df[map_stats_df['map_objective'] == objective_selection]
    options = su.set_options(objective_maps, 'map')
    map_selection = st.selectbox('Map', options)
else:
    objective_maps = map_stats_df
    options = su.set_options(objective_maps, 'map')
    map_selection = st.selectbox('Map', options)

if map_selection != 'All':
    su.display_map_stats(map_selection, map_stats_df, game_history_df)
else:
    for map in objective_maps['map']:
        su.display_map_stats(map, map_stats_df, game_history_df)
