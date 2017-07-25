from ehp import *

data = '''<body> <em> </em> </body>'''
html = Html()
dom  = html.feed(data)

font = Tag('font', {'color':'red'})
font.append(Data('Data inserted!'))

for ind in dom.find('em'):
    ind.append(font)

print(dom)


