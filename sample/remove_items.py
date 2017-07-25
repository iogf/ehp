from ehp import *

html = Html()

data = '''
<body> <em> foo </em> </body>
'''

dom = html.feed(data)

for root, item in dom.find_with_root('em'):
    root.remove(item)

print(dom)
