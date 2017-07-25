# Ehp

Easy Html Parser is an AST generator for html/xml documents. EHP is a nice tool to parse html content.  
It has a short learning curve compared to other parsers. You don't need to lose time going through massive 
documentation to do simple stuff. EHP handles broken html nicely.

EHP has a short learning curve, you can go through some examples, in a few minutes
you can implement cool stuff.

### Create/Delete elements

~~~python
from ehp import *

html = Html()

data = '''
<body> <em> foo </em> </body>
'''

dom = html.feed(data)

for root, item in dom.find_with_root('em'):
    root.remove(item)

print(dom)
~~~

~~~

<body >  </body>
~~~

### Manipulate attributes

~~~python
from ehp import *

data = '''<html><body> <p> It is simple.</p> </body></html>'''

dom = Html().feed(data)

for ind, name, attr in dom.walk():
    attr['size']  = '+2'

print(dom)
~~~

~~~
<html size="+2" ><body size="+2" > <p size="+2" > It is simple.</p> </body></html>
~~~

Install
=======

**Note:** Ehp works on python3 only, python2 support is no longer available.

~~~
pip setup.py install
~~~
    
**Note:** The module is quite well documented, you can find documentation there.





