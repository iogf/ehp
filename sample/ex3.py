# Name: ex3.py
from ehp import *


data  = '''<body> <em> </em> </body>'''
html = Html()
dom = html.feed(data)

for ind, name, attr in dom.walk():
    if  name == 'em': 
        x = Data('It is cool')
        ind.append(x)

print str(dom)






