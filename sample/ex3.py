from ehp import *

data = '''<body> <em> </em> </body>'''
dom  = Html().feed(data)

for ind in dom.find('em'):
    x = Data('It is cool')
    ind.append(x)

print dom
