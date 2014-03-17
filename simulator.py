#!/usr/bin/env python                                                           
import os
import json
import hashlib
import itertools
os.environ['DJANGO_SETTINGS_MODULE']='genetic_tac_toe.settings'

import genetic_tac_toe.settings
from django.conf import settings

from genetic_tac_toe.core.engine import Game


class AllGames(object):
    def __init__(self):
        self.all_perm = (game for game in itertools.permutations(tuple(range(1,10)),9))
        self.games_table = {}
    
    def play_all_games(self):
        n = 0
        for game in self.all_perm:
            self.simulate_game(game)
            n += 1
            if n % 1000 == 0:
                print n

    def simulate_game(self,moves):
        game = Game(self)
        for move,move_number in map(None,moves,range(1,len(moves)+1)):       
            piece = 'x' if bool(move_number % 2) else 'o'
            game.make_move(piece,num_pos=str(move))
            if game.won or game.draw:
                break
        self.save_move_data(game)

    def save_move_data(self,game):
        x_won = True if game.won == 'x' or game.draw else False
        finished_game_hash = hashlib.sha1(''.join(game.state_history)).hexdigest()
        if not finished_game_hash in self.games_table:
            self.games_table[finished_game_hash] = {'state':game.state_history,'x_won':x_won}

if __name__ == '__main__':
    games = AllGames()
    games.play_all_games()
    game_data = json.dumps(games.games_table)
    game_data_file = open('game_data.json','w')
    game_data_file.write(game_data)
    game_data_file.close()






