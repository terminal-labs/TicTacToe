

class Human(object):
    pass

class Computer(object):
    pass

class Game(object):
    def __init__(self):
        self.state = {
            'top':{'left':'','mid':'','right':''},
            'mid':{'left':'','mid':'','right':''},
            'bot':{'left':'','mid':'','right':''},
            }

    def make_move(self, y_pos, x_pos, player_piece='o'):
        assert self.state[y_pos][x_pos] == ''
        self.state[y_pos][x_pos] = player_piece
        


