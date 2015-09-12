from ehp import *

html = Html()
data = '''<tag> The &amp; is a good &amp; symbol. </tag>'''
dom = html.feed(data)

for root, ind in dom.find_with_root(AMP):
    if not ind.name == AMP: continue

    index = root.index(ind)
    root[index] = Data('ampersand')

print dom



