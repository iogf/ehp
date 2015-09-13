from ehp import *


data = '''<html> <body> <em> Hello world. </em>  
          <em style="color:blue"> It is a python. </em> </body> </html>'''

html = Html()
dom = html.feed(data)

for ind in dom.find('em'):
    print ind.text()


print dom.fst('em').text()
print dom.fst('body').text()
print dom.fst('html').text()

root, item = dom.take_with_root(('style', 'color:blue'))
print root
print item



