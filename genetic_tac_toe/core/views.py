import copy

from django.shortcuts import render

from engine import Game, Computer, Human



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
    print game.won, game.draw
    print grid
    return render(request, 'interface.html', {'grid':grid,'won':game.won,'draw':game.draw})

def render_move(request):
    if game.won or game.draw:
        return interface(request)
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
        print 2
        if request.GET.get('move','') == input:
            cord = key_mapping[input]
            if not game.won or game.draw:
                print 3
                game.make_move(cord[0],cord[1],'o')
                game.check_state()
            else:
                break

            if not game.won or game.draw:
                print 4
                game.compute_move()
                game.check_state()
            else:
                break

    print 555
    return interface(request)

def restart(request):
    global game
    game = Computer()
    game.compute_move()

    return interface(request)
