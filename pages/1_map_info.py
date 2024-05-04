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

