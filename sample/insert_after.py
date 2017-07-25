from ehp import *
data = '''<html><body><em> alpha </em></body></html>'''
dom = Html().feed(data)
x = Tag('em')
x.append(Data('beta'))

for root, ind in dom.find_with_root('em'):
    root.insert_after(ind, x)

print(dom)



