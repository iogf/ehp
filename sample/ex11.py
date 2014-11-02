from ehp import *

html = Html()
dom  = html.feed('''<body> <p style="color:black"> xxx </p> 
                 <p style = "color:black"> mmm </p></body>''')

for root, ind in dom.match_with_root(('style', 'color:black')):
    del ind.attr['style']

item = dom.fst('body')
item.attr['style'] = 'color:black'

print dom

