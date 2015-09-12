from ehp import *

data  = ''' <body><em> foo  </em></body>'''
html  = Html().feed(data)

for ind, name, attr in dom.walk():
    if not name == 'body': continue
    x = Tag('font', {'color':'red'})
    ind.append(x)

print dom




