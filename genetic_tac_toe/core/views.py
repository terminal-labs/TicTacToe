import copy

from django.shortcuts import render
from engine import Game



# Create your views here.


game = Game()

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
        print grid[column]
        for row in grid[column].keys():
            if grid[column][row] == 'x':
                grid[column][row] = x

            elif grid[column][row] == 'o':
                grid[column][row] = o

    return render(request, 'interface.html', {'grid':grid})

def render_move(request):
    key_mapping = {
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

    for input in map(lambda i: str(i),xrange(1,10)):
        if request.GET['move'] == input:
            cord = key_mapping[input]
            game.make_move(cord[0],cord[1])

    return interface(request)

def restart(request):
    global game
    game = Game()
    return interface(request)
