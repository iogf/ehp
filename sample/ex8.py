from ehp import *

data = '''<html> <body> <em> Hello world. </em> </body> </html>'''

html = Html()
dom = html.feed(data)

for ind in dom.find('em'):
    print ind.text()






