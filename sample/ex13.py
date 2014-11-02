from ehp import *
doc = Html()

tree = doc.feed(''' <html>
                        <body>
                            <em> alpha </em>
                        </body>
                    </html>
                ''')

for root, ind in tree.sail_with_root():
    if ind.name == 'em':
        x = Tag('em')
        root.insert_after(ind, x)

print tree

