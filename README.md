ehp
===

Easy Html Parser is an AST generator for html/xml documents. EHP is a nice tool to parse html content.  
It has a short learning curve compared to other parsers. You don't need to lose time going through massive 
documentation to do simple stuff. EHP handles broken html nicely.

EHP has a short learning curve, you can go through some examples, in a few minutes
you can implement cool stuff.

**remove_items.py**

~~~python
from ehp import *

html = Html()

data = '''
<body> <em> foo </em> </body>
'''

dom = html.feed(data)

for root, item in dom.find_with_root('em'):
    root.remove(item)

print dom
~~~

**Output:**

~~~

<body >  </body>
~~~

**insert_after.py**

~~~python
from ehp import *
data = '''<html><body><em> alpha </em></body></html>'''
dom = Html().feed(data)
x = Tag('em')
x.append(Data('beta'))

for root, ind in dom.find_with_root('em'):
    root.insert_after(ind, x)

print dom
~~~

**Output:**

~~~
<html ><body ><em > alpha </em><em >beta</em></body></html>
~~~

Install
=======
    pip2 setup.py install
    
That is all.

# Documentation

[Wiki](https://github.com/iogf/ehp/wiki)




