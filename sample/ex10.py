from ehp import *

html = Html()
dom = html.feed('''<body> <p> alpha </p> <p> beta </p> </body>''')

for root, ind in dom.find_with_root('p'):
    root.remove(ind)

print dom




