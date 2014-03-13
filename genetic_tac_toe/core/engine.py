import random

class Game(object):
    def __init__(self):
        self.state = {
            'top':{'left':'','mid':'','right':''},
            'mid':{'left':'','mid':'','right':''},
            'bot':{'left':'','mid':'','right':''},
            }
        self.won = False
        self.draw = False

    def make_move(self, y_pos, x_pos, player_piece):
        assert self.state[y_pos][x_pos] == ''
        assert player_piece == 'x' or player_piece == 'o'
        self.state[y_pos][x_pos] = player_piece

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
        
        


