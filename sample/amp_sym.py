from ehp import *

html = Html()
data = '''<tag> The &amp; is a good &amp; symbol. </tag>'''
dom = html.feed(data)

for root, ind in dom.find_with_root(AMP):
    print(ind)

