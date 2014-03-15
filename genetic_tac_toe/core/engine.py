import copy
import random
import hashlib

from models import MoveHash, Moves

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

    def make_move(self, y_pos, x_pos, player_piece):
        assert 0 <= len(self.state_history) <= 9
        assert self.state[y_pos][x_pos] == ''
        assert player_piece == 'x' or player_piece == 'o'
        self.state[y_pos][x_pos] = player_piece
        self.state_history += tuple(filter(lambda x: self.key_mapping[x][0] == y_pos and self.key_mapping[x][1] == x_pos, self.key_mapping))

    def save_move_data(self):
        x_won_game = True if self.won == 'x' or self.draw else False

        hist = copy.deepcopy(self.state_history)
        while len(hist) < 9:
            print 'Noooooooooo!!!!!!!!!'
            hist += ('0',)
        finished_game_hash = hashlib.sha1(''.join(self.state_history)).hexdigest()
        if not MoveHash.objects.filter(move_hash=finished_game_hash).exists():
            this_game = Moves.objects.create(
                move_1=hist[0],move_2=hist[1],move_3=hist[2],
                move_4=hist[3],move_5=hist[4],move_6=hist[5],
                move_7=hist[6],move_8=hist[7],move_9=hist[8],
                x_won_game=x_won_game)

            import time
            for move, move_number in map(None,self.state_history,range(1,len(self.state_history)+1)):
                print ''.join(self.state_history[:move_number])
                move_hash = hashlib.sha1(''.join(self.state_history[:move_number])).hexdigest()
                x = time.time()
                if not MoveHash.objects.filter(move_hash=move_hash).exists():
                    print time.time() - x,1
                    x= time.time()
                    permutation_hash = MoveHash.objects.create(move_number=move_number,move_hash=move_hash)
                    print time.time() -x,2
                    x= time.time()
                    permutation_hash.save()
                    print time.time() -x,3
                else:
                    x = time.time()
                    permutation_hash = MoveHash.objects.get(move_hash=move_hash)
                    print time.time(),4
                this_game.move_hash.add(permutation_hash)
            this_game.save()

    def check_state(self):
        def all_same(elements):
            return all(ele == elements[0] for ele in elements)
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

        if self.won or self.draw:
            self.save_move_data()

class Computer(Game):
    def compute_move(self):
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

        self.make_move(y_pos, x_pos, 'x')
        
        


