# Name: ex4.py

from ehp import *

html = Html()

data = '''
<body> <em> foo </em> </body>
'''

dom = html.feed(data)

for root, item in dom.sail_with_root():
    if item.name == 'em':
        root.remove(item)
        x = Tag('p')
        x.append(Data('foo'))
        root.append(x)

print dom





