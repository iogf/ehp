from ehp import *

data  = ''' <body><em> foo  </em></body>'''
dom  = Html().feed(data)

for ind in dom.find('em'):
    x = Tag('font', {'color':'red'})
    ind.append(x)

print dom
