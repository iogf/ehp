# Name: ex9.py

from ehp import *


data = '''<html> <body> 
          <em style="background:blue"> It is a python. </em> 
          </body> </html>'''

html = Html()
dom = html.feed(data)

for ind in dom.match(('style', 'background:blue')):
    print ind.text()


for ind in dom.match(('style', 'background:blue'),
                      ('onclick', 'foo();')):

    # It shouldn't be printed.
    print ind.text()





