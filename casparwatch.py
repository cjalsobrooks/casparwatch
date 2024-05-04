import streamlit as st
import pandas as pd
import random
import map_hero_choices as mh
import stat_util as su

# set up dfs
game_history_df = pd.read_csv('data/game_history.csv')
hero_stats_df = pd.DataFrame(columns=['hero','role','win_percentage','games_played','games_won','games_lost','games_drawn','best_map'])
map_stats_df = pd.DataFrame(columns=['map','win_percentage','games_played','games_won','games_lost','games_drawn','best_hero', 'map_objective'])

# const options for entry creation
maps = mh.MAPS.keys()
heroes = mh.HEROES.keys()
outcomes = mh.OUTCOMES
modes = mh.MODES

# overall WR
total_games = len(game_history_df)     
win_count = (game_history_df['outcome'] == 'W').sum()
win_percentage = round(win_count / total_games * 100,1)

# fill hero stat df
unique_heroes = game_history_df.sort_values(by='hero', ascending=True)['hero'].unique()
for hero in unique_heroes:
    hero_games = game_history_df[game_history_df['hero'] == hero]
    hero_role = mh.HEROES.get(hero)

    # win, loss, draw, wp   
    hero_total_games = len(hero_games)     
    hero_win_count = (hero_games['outcome'] == 'W').sum()
    hero_loss_count = (hero_games['outcome'] == 'L').sum()
    hero_draw_count = (hero_games['outcome'] == 'D').sum()
    hero_win_percentage = round((hero_win_count / hero_total_games) * 100, 1)

    #best map based on wp
    map_win_dict = su.get_map_by_hero(hero, game_history_df)
    hero_best_map = max(map_win_dict, key=map_win_dict.get)
    hero_stats_df = pd.concat([hero_stats_df, pd.DataFrame([{'hero':hero,'role':hero_role,'win_percentage':hero_win_percentage, 'games_played':hero_total_games, 'games_won':hero_win_count, 'games_lost':hero_loss_count, 'games_drawn':hero_draw_count, 'best_map':hero_best_map}])], ignore_index=True)

# fill map stat df
unique_maps = game_history_df.sort_values(by='map', ascending=True)['map'].unique()
for map in unique_maps:
    map_games = game_history_df[game_history_df['map'] == map]
    map_objective = mh.MAPS.get(map)

    # win, loss, draw, wp
    map_games_played = len(map_games)
    map_games_won = (map_games['outcome'] == 'W').sum()
    map_games_lost = (map_games['outcome'] == 'L').sum()
    map_games_drawn = (map_games['outcome'] == 'D').sum()
    map_win_percentage = round((map_games_won / map_games_played) * 100)

    hero_win_dict = su.get_hero_by_map(map, game_history_df)
    map_best_hero = max(hero_win_dict, key=hero_win_dict.get)
    map_stats_df = pd.concat([map_stats_df, pd.DataFrame([{'map':map, 'win_percentage':map_win_percentage, 'games_played':map_games_played, 'games_won':map_games_won, 'games_lost':map_games_lost, 'games_drawn':map_games_drawn, 'best_hero':map_best_hero, 'map_objective':map_objective}])], ignore_index=True)

#display win rate and shame user LOL + add new entries
title, button = st.columns([0.6,1])
with title:
    st.title('Stat Overview')

with button:
    st.write('')
    with st.expander('Add new game'):
        map_input = st.selectbox("Select Map", mh.MAPS.keys())
        hero_input = st.selectbox("Select Hero", mh.HEROES.keys())
        outcome_input = st.selectbox("Select Outcome", mh.OUTCOMES)
        mode_input = st.selectbox("Select Mode", mh.MODES)
        if st.button('Submit'):
            game_history_df = pd.concat([game_history_df, pd.DataFrame([{'map':map_input, 'hero':hero_input, 'outcome':outcome_input, 'mode':mode_input}])], ignore_index=True)

st.header('Your overall win rate is ' + str(win_percentage) + "%.")
if win_percentage > 50:
    message = 'Great job champ! Keep it up. People wish they were you.'
elif win_percentage > 30:
    message = "You can and should get better hehe! But remember, it's always your teammates fault."
else:
    message = "Well, this is a little embarassing. But don't worry! I'm sure you have strengths that don't involve a keyboard and mouse."
st.write(message)

# fun stats about best hero
best_hero_stats = su.get_best_wr(hero_stats_df)
best_hero_map_dict = su.get_map_by_hero(best_hero_stats['hero'], game_history_df)
best_hero_best_map = max(best_hero_map_dict, key=best_hero_map_dict.get)
best_hero_worst_map = min(best_hero_map_dict, key=best_hero_map_dict.get)
st.header('Your best hero is ' + best_hero_stats['hero'] + " with a win rate of " + str(best_hero_stats['win_percentage']) + '%.')
st.write('You and ' + best_hero_stats['hero'] + ' were a match made in heaven on ' + best_hero_best_map + ", but you should be cast into hell the next time you try to play them on " + best_hero_worst_map + ".")

#fun stats about best map
best_map_stats = su.get_best_wr(map_stats_df)
best_map_hero_dict = su.get_hero_by_map(best_map_stats['map'], game_history_df)
best_map_best_hero = max(best_map_hero_dict, key=best_map_hero_dict.get)
best_map_worst_hero = min(best_map_hero_dict, key=best_map_hero_dict.get)
st.header('Your best map is ' + best_map_stats['map'] + " with a win rate of " + str(best_map_stats['win_percentage']) + '%.')
st.write('You did your best work on  '+ best_map_stats['map'] + " while playing " + best_map_best_hero + '. That being said, we\'ll be banning you from touching ' + best_map_worst_hero + " within 100 miles of the premises.")

#display most recent 10 games


st.header('Latest Games:')
mode_selection = st.selectbox('Modes', ['All Games', 'Competitive', 'Unranked'])
if mode_selection != 'All Games':
    recent = game_history_df[game_history_df['mode'] == mode_selection].tail(10)
else:
    recent = game_history_df.tail(10)
recent

#update csv
game_history_df.to_csv('data/game_history.csv', sep=',',index=False)
hero_stats_df.to_csv('data/hero_stats.csv', sep=',',index=False)
map_stats_df.to_csv('data/map_stats.csv', sep=',', index=False)



