from django.shortcuts import render

# Create your views here.

def interface( request ):
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
    grid = {
        'top':{'left':'','mid':'','right':''},
        'mid':{'left':'','mid':'','right':''},
        'bot':{'left':'','mid':'','right':''},
        }
    grid['top']['left'] = x
    grid['mid']['mid'] = x
    grid['bot']['right'] = x
    

    return render(request, 'interface.html', {'grid':grid})
