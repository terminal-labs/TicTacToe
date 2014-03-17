import copy
import json
import random
import hashlib

try:
    print 'Loading Data...'
    game_data_file = open('game_data.json')
    game_data = json.loads(game_data_file.read())
    game_data_file.close()
    smart = True
    print 'Done'
    print 'Running in smart mode'
except IOError:
    print 'Data not loaded!'
    smart = False

class Game(object):
    def __init__(self):
        self.state = { 
            'top':{'left':'','mid':'','right':''},
            'mid':{'left':'','mid':'','right':''},
            'bot':{'left':'','mid':'','right':''},
            }

        self.key_mapping = {
            '1':('bot','left'),
            '2':('bot','mid'),
            '3':('bot','right'),
            '4':('mid','left'),
            '5':('mid','mid'),
            '6':('mid','right'),
            '7':('top','left'),
            '8':('top','mid'),
            '9':('top','right'),
            }

        self.state_history = ()

        self.won = False
        self.draw = False

    def hist(self):
        return copy.deepcopy(self.state_history)

    def make_move(self, player_piece, y_pos=None, x_pos=None, num_pos=None):
        assert bool(y_pos and x_pos) ^ bool(num_pos)
        if num_pos:
            y_pos,x_pos = self.key_mapping[str(num_pos)]
        assert 0 <= len(self.state_history) <= 9
        assert self.state[y_pos][x_pos] == ''
        assert player_piece == 'x' or player_piece == 'o'
        pieces = self.state['top'].values() + self.state['mid'].values() + self.state['bot'].values()
        assert pieces.count('x') == pieces.count('o') or pieces.count('x') == pieces.count('o') + 1
        self.state[y_pos][x_pos] = player_piece
        self.state_history += tuple(filter(lambda x: self.key_mapping[x][0] == y_pos and self.key_mapping[x][1] == x_pos, self.key_mapping))
        self.check_state()

    def check_state(self):
        def all_same(elements):
            if all(ele == elements[0] for ele in elements):
                if elements[0] == 'x' or elements[0] == 'o':
                    return True
            return False
        winning_row = filter(lambda row: all_same(self.state[row].values()) ,self.state)
        ## Check the rows
        if winning_row:
            winner = self.state[winning_row[0]]['left']
            self.won = winner

        ## Check the columns
        for col in self.state['top'].keys():
            if all_same(map(lambda x: self.state[x][col], self.state)):
                winner = self.state['top'][col]
                self.won = winner

        ## Check a diaganol
        if all_same([self.state['top']['left'],self.state['mid']['mid'],self.state['bot']['right']]):
            winner = self.state['mid']['mid']
            self.won = winner

        ## Check the other diaganol
        if all_same([self.state['top']['right'],self.state['mid']['mid'],self.state['bot']['left']]):
            winner = self.state['mid']['mid']
            self.won = winner

        ## Check for draw
        if len(filter(lambda x: all(self.state[x].values()),self.state)) == 3 and not self.won:
            self.draw = True

class Computer(Game):
    def compute_move(self):
        ## Take the Middle
        if not self.state['mid']['mid']:
            self.make_move('x',num_pos='5')
            return

        if self.state_history == ('5','1'):
            self.make_move('x',num_pos='9')
            return

        ## Can I win now?
        for row in self.state.keys():
            if self.state[row].values().count('x') == 2 and self.state[row].values().count('o') == 0:
                x_pos = filter(lambda i: not self.state[row][i],self.state[row].keys())[0]
                self.make_move('x',y_pos=row,x_pos=x_pos)
                return

        for x_pos in self.state['top'].keys():
            col = [self.state['top'][x_pos], self.state['mid'][x_pos], self.state['bot'][x_pos]]
            if col.count('x') == 2 and col.count('o') == 0:
                for row in self.state.keys():
                    if not self.state[row][x_pos]:
                        self.make_move('x',y_pos=row,x_pos=x_pos)
                        return


        dig1 = [self.state['top']['left'], self.state['mid']['mid'], self.state['bot']['right']]
        if dig1.count('x') == 2 and dig1.count('o') == 0:
            if not self.state['top']['left']:
                self.make_move('x',y_pos='top',x_pos='left')
                return

            if not self.state['mid']['mid']:
                self.make_move('x',y_pos='mid',x_pos='mid')
                return

            if not self.state['bot']['right']:
                self.make_move('x',y_pos='bot',x_pos='right')
                return

        dig2 = [self.state['top']['right'], self.state['mid']['mid'], self.state['bot']['left']]
        if dig2.count('x') == 2 and dig1.count('o') == 0:
            if not self.state['top']['right']:
                self.make_move('x',y_pos='top',x_pos='right')
                return

            if not self.state['mid']['mid']:
                self.make_move('x',y_pos='mid',x_pos='mid')
                return

            if not self.state['bot']['left']:
                self.make_move('x',y_pos='bot',x_pos='left')
                return

        ## Can my opponent win?
        for row in self.state.keys():
            if self.state[row].values().count('x') == 0 and self.state[row].values().count('o') == 2:
                x_pos = filter(lambda i: not self.state[row][i],self.state[row].keys())[0]
                self.make_move('x',y_pos=row,x_pos=x_pos)
                return

        for x_pos in self.state['top'].keys():
            col = [self.state['top'][x_pos], self.state['mid'][x_pos], self.state['bot'][x_pos]]
            if col.count('x') == 0 and col.count('o') == 2:
                for row in self.state.keys():
                    if not self.state[row][x_pos]:
                        self.make_move('x',y_pos=row,x_pos=x_pos)
                        return



        if not smart:
            '''
            This is a dummy AI I have in place while completing a working interface.
            It simply randomly picks a free space on the grid. It does NOT at all
            satisfy the requierment that it never loses.
            '''
            if self.won or self.draw:
                return
            pos = 1
            while True:
                y_pos = random.choice(self.state.keys())
                x_pos = random.choice(self.state[y_pos].keys())
                pos = self.state[y_pos][x_pos]
                if pos == '':
                    break
            self.make_move('x',y_pos=y_pos, x_pos=x_pos)
            return

        elif smart:
            possible_moves = self.possible_moves()
            move_number = len(self.state_history) + 1
            for possible_game in self.generate_possilbe_games(possible_moves):
                possible_moves = self.possible_moves(possible_game)
                state_hash = self.gen_hash(possible_game)
                try:
                    if game_data[state_hash]['x_won']:
                        self.make_move('x',num_pos=possible_game[move_number - 1])
                        return
                except KeyError:
                    pass

                for possible_game in self.generate_possilbe_games(possible_moves,hist=possible_game):
                    possible_moves = self.possible_moves(possible_game)

                    for possible_game in self.generate_possilbe_games(possible_moves,hist=possible_game):
                        state_hash = self.gen_hash(possible_game)
                        try:
                            if game_data[state_hash]['x_won']:
                                self.make_move('x',num_pos=possible_game[move_number - 1])
                                return
                        except KeyError:
                            pass
                
    def possible_moves(self,state=None):
        if not state:
            return filter(lambda i: i,[str(move) if move not in map(int,self.state_history) else None for move in tuple(range(1,10))])
        else:
            return filter(lambda i: i,[str(move) if move not in map(int,state) else None for move in tuple(range(1,10))])

    def generate_possilbe_games(self,possible_moves,hist=None):
        if not hist:
            hist = self.hist()
        for move in possible_moves:
            possible_state = hist + (move,)
            yield possible_state
                    
    def gen_hash(self,state=None):
        if not state:
            return hashlib.sha1(''.join(self.state_history)).hexdigest()
        else:
            return hashlib.sha1(''.join(map(str,state))).hexdigest()
