from ehp import *

data = '''<html><body> <font size="+3" > <p> It is simple.</p> 
</font> </body></html>'''

dom = Html().feed(data)

for ind, name, attr in dom.walk():
    attr['size']  = '+2'
    attr['color'] = 'red'

print dom



