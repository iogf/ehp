from ehp import *

html = Html()

data = '''
<p>
This is a paragraph.
</p>
'''

dom = html.feed(data)

print("The entire dom:")
print(dom)
print("The text in the dom:")
print(dom.text())






