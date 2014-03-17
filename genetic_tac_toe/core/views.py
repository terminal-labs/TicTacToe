import copy

from django.shortcuts import render

from engine import Game, Computer



# Create your views here.


game = Computer()

def interface(request):
    
    x = '''
?88,  88P
 `?8bd8P'
 d8P?8b, 
d8P' `?8b
'''
    o = '''
 d8888b 
d8P' ?88
88b  d88
`?8888P'
'''    

    grid = copy.deepcopy(game.state)
    for column in grid.keys():
        for row in grid[column].keys():
            if grid[column][row] == 'x':
                grid[column][row] = x

            elif grid[column][row] == 'o':
                grid[column][row] = o
    return render(request, 'interface.html', {'grid':grid,'won':game.won,'draw':game.draw})

def render_move(request,move=None):
    if game.won or game.draw:
        return interface(request)
    if move in map(str,range(1,10)):
        if not game.won or game.draw:
            game.make_move('o',num_pos=move)
        if not game.won or game.draw:
            game.compute_move()

    return interface(request)

def restart(request):
    global game
    game = Computer()
    game.compute_move()

    return interface(request)
