# Name: ex-2.py

from ehp import *


data = '''
<font size="+3" > <p> It is simple.</p> </font> 
<font size="+1" > <p> It is powerful</p></font>'''

html = Html()
dom = html.feed(data)

for ind, name, attr in dom.walk():
    if name == 'font':
        if attr['size'] == '+1':    attr['color'] = 'red'
        elif attr['size'] == '+3':  attr['color'] = 'blue'

print dom

