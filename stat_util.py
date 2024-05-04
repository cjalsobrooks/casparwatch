import streamlit as st
import re #regex
import pandas as pd


#use to get the highest win rate in a given df 
def get_best_wr(df):
    best_wr = df['win_percentage'].idxmax()
    best_wr = df.loc[best_wr]
    return best_wr

#use to get a dictionary of map win rates by hero
def get_map_by_hero(hero, game_history):
    hero_games = game_history[game_history['hero'] == hero]
    unique_maps = hero_games.sort_values(by='map', ascending=True)['map'].unique()
    map_win_dict = {}

    for map in unique_maps:
        map_games = hero_games[hero_games['map'] == map]

        map_total_games = len(map_games)
        map_win_count = (map_games['outcome'] == 'W').sum()
        map_win_percentage = (map_win_count / map_total_games) * 100
        map_win_dict.update({map: map_win_percentage})

    return map_win_dict

#use to get a dictionary of hero win rates by map
def get_hero_by_map(map, game_history):
    map_games = game_history[game_history['map'] == map]
    unique_heroes = map_games.sort_values(by='hero', ascending=True)['hero'].unique()
    hero_win_dict = {}

    for hero in unique_heroes:
        hero_games = map_games[map_games['hero'] == hero]

        hero_total_games = len(hero_games)
        hero_win_count = (hero_games['outcome'] == 'W').sum()
        hero_win_percentage = (hero_win_count / hero_total_games) * 100
        hero_win_dict.update({hero: hero_win_percentage})

    return hero_win_dict

#use to display hero stats
def display_hero_stats(hero_selection, hero_stats_df, game_history_df):
    name, icon, placeholder = st.columns([0.2, 0.3, 0.5])
    with icon:
        image_path = get_filepath(hero_selection)
        try:
            st.image(image_path, use_column_width=True)
        except:
            st.image('pics/sad_file_not_found.png', caption='File not found', use_column_width=True)
    with name:
        vertical_align(5)
        st.header(hero_selection)

    selected_hero_stats = hero_stats_df[hero_stats_df['hero'] == hero_selection]

    title, stat = st.columns([0.4, 1])
    with title:
        st.subheader('Win Percentage')
        st.subheader('Games Played')
        st.subheader('Maps')

    with stat:
        st.write('')
        st.write('Your winrate is ' + str(selected_hero_stats['win_percentage'].iloc[0]) + '%.')

        st.write('')
        w = str(selected_hero_stats['games_won'].iloc[0])
        l = str(selected_hero_stats['games_lost'].iloc[0])
        d = str(selected_hero_stats['games_drawn'].iloc[0])
        gp = str(selected_hero_stats['games_played'].iloc[0])
        st.write('You have played ' + gp + ' games. (' + w + 'W/' + l + 'L/' + d + 'D)')

        map_stats = get_map_by_hero(hero_selection, game_history_df)
        best = max(map_stats, key=map_stats.get)
        worst = min(map_stats, key=map_stats.get)
        st.write('Your best map is ' + best + '. Your worst map is ' + worst + '. Below are your win percentages for each map.')
        map_stats_df = pd.DataFrame.from_dict(map_stats, orient='index', columns=['WR'])
        st.write(map_stats_df)

def display_map_stats(map, map_stats, game_history):
    selected_map_stats = map_stats[map_stats['map'] == map]
    
    name, icon, placeholder = st.columns([0.3, 0.3, 0.4])
    with icon:
        map_objective = selected_map_stats['map_objective'].iloc[0]
        image_path = get_filepath(map_objective)
        try:
            st.image(image_path, use_column_width=True)
        except:
            st.image('pics/sad_file_not_found.png', caption='File not found', use_column_width=True)
    with name:
        vertical_align(4)
        st.header(map)

    title, stat = st.columns([0.4, 1])
    with title:
        st.subheader('Win Percentage')
        st.subheader('Games Played')
        st.subheader('Heroes')

    with stat:
        st.write('')
        st.write('Your winrate is ' + str(selected_map_stats['win_percentage'].iloc[0]) + '%.')

        st.write('')
        w = str(selected_map_stats['games_won'].iloc[0])
        l = str(selected_map_stats['games_lost'].iloc[0])
        d = str(selected_map_stats['games_drawn'].iloc[0])
        gp = str(selected_map_stats['games_played'].iloc[0])
        st.write('You have played ' + gp + ' games. (' + w + 'W/' + l + 'L/' + d + 'D)')

        hero_stats = get_hero_by_map(map, game_history)
        best = max(hero_stats, key=hero_stats.get)
        worst = min(hero_stats, key=hero_stats.get)
        st.write('Your best hero for this map is ' + best + '. Your worst hero for this map is ' + worst + '. Below are your win percentages for each hero.')
        hero_stats_df = pd.DataFrame.from_dict(hero_stats, orient='index', columns=['WR'])
        st.write(hero_stats_df)

#use to create a select box with a default all option
def set_options(df, column):
    options = ['All']
    col_values = df[column]
    for val in col_values:
        options.append(val)
    return options

#use to lower element
def vertical_align(num):
    for i in range(num):
        st.write('')

#use to get file path for hero pngs
def get_filepath(hero):
    pattern = r'[^A-Za-z]+'
    hero = re.sub(pattern, '', hero).lower()
    image_path = 'pics/' + hero + '.png'
    return image_path