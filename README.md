ehp
===

Easy Html Parser is an AST generator for html/xml documents. EHP is a nice tool to parse html content.  
It has a short learning curve compared to other parsers. You don't need to lose time going through massive 
documentation to do simple stuff. EHP handles broken html nicely.

EHP has a short learning curve, you can go through some examples, in a few minutes
you can implement cool stuff.

Install
=======
    python setup.py install
    
That is all.

A simple example
=================

~~~python
from ehp import *

data = '''<html><body> <font size="+3" > <p> It is simple.</p> 
</font> </body></html>'''

dom = Html().feed(data)

for ind, name, attr in dom.walk():
    if not name == 'font': continue
    attr['size']  = '+2'
    attr['color'] = 'red'

print dom
~~~    

**Output:**

~~~
<html ><body > <font color="red" size="+2" > <p > It is simple.</p> 
</font> </body></html>
~~~

The Html class is responsible by parsing html content. The Html.feed method returns a DOM representation 
of the html document. The html elements are represented by classes whose methods permit to manipulate such
elements, changing their attributes, adding new elements, removing elements. 

~~~python
class Tag(Root)
 |  This class's instances represent xml/html tags under the form:
 |  <name key="value" ...> ... </name>.
 |  
 |  It holds useful methods for parsing xml/html documents.
.
.
.
~~~

The above class is responsible by representing most of the html elements. Such a class has methods
to insert, delete, html elements. The Tag class inherits from Root that abstracts all useful characteristics
of all html elements. It is possible to create new tags with attributes then insert them between specific
positions as shown in the example below.

~~~python
from ehp import *

data  = ''' <body><em> foo  </em></body>'''
html  = Html().feed(data)

for ind, name, attr in dom.walk():
    if not name == 'body': continue
    x = Tag('font', {'color':'red'})
    ind.append(x)

print dom
~~~

**Output.**

~~~
<html ><body > <font color="red" size="+2" > <p > It is simple.</p> 
</font> <font color="red" ></font></body></html>
~~~

Most of the html elements may hold text, all classes have a method to retrieve raw data.
The example below shows the usage of the Root.find and Root.text methods.

~~~python
from ehp import *

data = '''<html> <body> <em> Hello world. </em> </body> </html>'''

html = Html()
dom = html.feed(data)

for ind in dom.find('em'):
    print ind.text()
~~~

**Output:*

~~~
 Hello world. 
~~~

The find method returns an interator whose elements's names are matching with the passed argument. The Root.find
method is useful when it is known which element we need.

It is possible to remove specific elements by using the Root.remove method. The example below shows how to use such
a method.

~~~python
from ehp import *

html = Html()
dom = html.feed('''<body> <p> alpha </p> <p> beta </p> </body>''')

for root, ind in dom.find_with_root('p'):
    root.remove(ind)

print dom
~~~

**Output:**

~~~
<body >   </body>
~~~

The method Root.find_with_root is used to iterate over the html elements while yielding their outmost elements.
The example shown above iterates over all tags whose name match with 'p' then remove them from the outmost
tag that is 'body'.

It is possible to iterate over elements whose attributes match a given condition as follow below.

~~~python
data = '<body><a size="2"><b size="1"></b></a></body>'
html = Html()
dom = html.feed(data)

for ind in dom.match(('size', '1')):
    print ind
~~~

**Output:**

~~~
<b size="1" ></b>
~~~

There is a Root.match_with_root in all classes whose purpose is returning an iterator with
html elements matching an attribute condition and their outmost tags.

There are classes to abstract special html entites like the Amp, Meta, Code, Comment, Pi.

~~~python
from ehp import *

html = Html()
data = '''<tag> The &amp; is a good &amp; symbol. </tag>'''
dom = html.feed(data)

for root, ind in dom.find_with_root(AMP):
    if not ind.name == AMP: continue

    index = root.index(ind)
    root[index] = Data('ampersand')

print dom
~~~

The Root.index method is used to return the tag's index in relation to its outmost tag. It is possible to insert
raw data inside html elements by instantiating the class Data with data.

**Output:**

~~~
<tag > The &amp is a good &amp symbol. </tag>
~~~

Help
====

If you have sugestions or need help you can find me at irc.freenode.org
channel #vy.

You can contact me through email as well.
ioliveira@id.uff.br


