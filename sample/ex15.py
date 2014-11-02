from ehp import *

data = '<body> <p> alpha. </p> <p style="color:green"> beta.</p> </body>'
html = Html()
dom  = html.feed(data)

for ind in dom.find('p', ('style', 'color:green')):
    print ind

print dom.fst('p', ('style', 'color:green'))
print dom.fst_with_root('p', ('style', 'color:green'))
