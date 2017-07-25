# Name: ex17.py

from ehp import *

html = Html()
data = '<body> <em> beta. </em></body>'
dom = html.feed(data)

root, item = dom.fst_with_root('em')
root.insert_after(item, Tag('p'))
print(root)




