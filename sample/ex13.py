from ehp import *
data = '''<html><body><em> alpha </em></body></html>'''
dom = Html().feed(data)

for root, ind in dom.find_with_root('em'):
    x = Tag('em')
    x.append(Data('cool'))
    root.insert_after(ind, x)

print dom


