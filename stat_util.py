def get_best_wr(df):
    best_wr = df['win_percentage'].idxmax()
    best_wr = df.loc[best_wr]
    return best_wr

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