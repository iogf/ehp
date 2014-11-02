from ehp import *

data  = ''' <body><em> foo  </em></body>'''
html  = Html()
dom  = html.feed(data)


for ind in dom.sail():
    if ind.name == 'body':
        x = Tag('font', {'color':'red'})
        ind.append(x)


print str(dom)



