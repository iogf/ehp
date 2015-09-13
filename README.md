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

Print the DOM object
====================

~~~python
from ehp import *

html = Html()

data = '''
<p>
This is a paragraph.
</p>
'''


dom = html.feed(data)
print dom
~~~    

**Output:**

~~~
<p >
This is a paragraph.
</p>
~~~

That above example shows how to generate a tree representation for html content. The Html class is the parser class it implements
the Html.feed method which is used to build a tree representation for html content that is passed through a string. All classes
that map a html entity have a __str__ method.

Walking through the tree
========================

~~~python
from ehp import *

data = '''<html><body> <font size="+3" > <p> It is simple.</p> 
</font> </body></html>'''

dom = Html().feed(data)

for ind, name, attr in dom.walk():
    attr['size']  = '+2'
    attr['color'] = 'red'

print dom
~~~

**Output.**

~~~
<html color="red" size="+2" ><body color="red" size="+2" > <font color="red" size="+2" > <p color="red" size="+2" > It is simple.</p> 
</font> </body></html>
~~~

The example shows how to walk through all html entities and manipulate their attributes. The variable ind in that
example holds the tree representation a html entity that is being visited. The variable name holds the visited html entity name
and the attr variable holds a dictionary whose keys are html entity attributes.

Find specific html entities
============================

~~~python
from ehp import *

data = '''<body> <em> </em> </body>'''
dom  = Html().feed(data)

for ind in dom.find('em'):
    x = Data('It is cool')
    ind.append(x)

print dom
~~~

**Output:*

~~~
<body > <em > It is cool</em> </body>
~~~

This example shows how to visit html entities whose names match a given string. Notice it is possible
to add new html entites to the html by instantiating the class Tag, XTag, Data, Amp etc.
All objects used to represent html entities inherit from python list class so they all have
a method list.append.

Remove a specific html entity
=============================

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

That example shows how to use the Root.find_with_root method to match html entities with specific html types and
how to remove them from the outmost html entity. The Root.find_with_root method returns an iterator
holding the outmost html entity for a node being visited.

Insert a new html entity
========================

~~~python
from ehp import *

data  = ''' <body><em> foo  </em></body>'''
dom  = Html().feed(data)

for ind in dom.find('em'):
    x = Tag('font', {'color':'red'})
    ind.append(x)

print dom
~~~

**Output:**

~~~
 <body ><em > foo  <font color="red" ></font></em></body>
~~~

The example shown above examplifies how to insert a new html entity in a tree representation. 

Retrieve raw data
=================

~~~python
from ehp import *

data = '''<html> <body> <em> Hello world. </em> </body> </html>'''

html = Html()
dom = html.feed(data)

for ind in dom.find('em'):
    print ind.text()
~~~

**Output:**

~~~
 Hello world. 
~~~

That one shows the usage of the Root.text method that is used to retrieve all raw data from html entities.
The Root class abstracts all common methods of html entities, all classes mapping html entities inherit from Root.

Attribute based condition
=========================

~~~python
from ehp import *

data = '''<html> <body> 
          <em style="background:blue"> It is a python. </em> 
          <p> cool </p></body> </html>'''

dom = Html().feed(data)

for ind in dom.match(('style', 'background:blue')):
    print ind.text()

~~~

**Output:**

~~~
 It is a python. 
~~~

The above example shows how to visit html entities that match a given attribute condition. It is very useful
sometimes.

The Amp, Meta, Code, Comment, Pi, Data classes
==============================================

~~~python
from ehp import *

html = Html().feed(data)
data = '''<tag> The &amp; is a good &amp; symbol. </tag>'''
dom = html.feed(data)

for root, ind in dom.find_with_root(AMP):
    print ind
~~~

**Output:**

~~~
&amp
&amp
~~~

There are special classes in EHP that represent special html elements. These classes are
Amp, Meta, Code, Comment and Data. 

The AMP, DATA, META, CODE, COMMENT values are the names of such entities in EHP. 
One would call the Root.find method with a string or with one of these values to find nodes. 

The DATA name means it is raw data, CODE means hexadecimal numeric characters, COMMENT means html comments,  Pi means processing instructions
like ~~~ <?proc color='red'> ~~~ , META means html doctypes.

There are other handy methods to manipulate a tree html representation, for help on these methods
see the EHP built-in docs.

Help
====

If you have sugestions or need help you can find me at irc.freenode.org
channel #vy.

You can contact me through email as well.
ioliveira@id.uff.br






