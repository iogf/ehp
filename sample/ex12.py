from ehp import *


data = '''<html> <body> 
          <em style="background:blue"> It is a python. </em> 
          <p> cool </p></body> </html>'''

dom = Html().feed(data)

for ind in dom.match(('style', 'background:blue')):
    print ind.text()

