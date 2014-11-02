ehp
===

Easy Html Parser is an AST generator for html/xml documents. You can easily delete/insert/extract tags in html/xml documents as well as look for patterns.

Easy html parser EHP is a nice tool to parse html content. 
It has a short learning curve. It builds a DOM representation for html documents,
the DOM classes have powerful methods to insert, delete and change html attributes.

EHP has a short learning curve, you can go through some examples, in a few minutes
you can implement cool stuff.

Install
=======
    python setup.py install
    
That is all.

Examples
========
A simple example.

    from ehp import *
    
    # The parser class.
    html = Html()
    
    data = '''
    <p>
    This is a paragraph.
    </p>
    '''
    
    # The feed method builds a DOM structure for the html document.
    dom = html.feed(data)
    print dom
    
Output.

    <p >
    This is a paragraph.
    </p>
    

Walking through the dom and changing html tag attributes.
    from ehp import *
    
    data = '''
    <font size="+3" > <p> It is simple.</p> </font> 
    <font size="+1" > <p> It is powerful</p></font>'''
    
    # The parser class.
    html = Html()

    # The DOM structure.
    dom = html.feed(data)
    
    for ind, name, attr in dom.walk():
        # If the tag name is font we then check their
        # attributes.

        if name == 'font':
            if attr['size'] == '+1':    
                # If size matches the condition 
                # then we add a new attribute.
        
                attr['color'] = 'red'
            elif attr['size'] == '+3':  

                attr['color'] = 'blue'
    
    print dom
    

Output.
    <font color="blue" size="+3" > <p > It is simple.</p> </font> 
    <font color="red" size="+1" > <p > It is powerful</p></font>
    

Add new html tags to the DOM structure.
This example inserts text between the tags <em> </em>

    data  = '''<body> <em> </em> </body>'''
    html = Html()
    dom = html.feed(data)
    
    for ind, name, attr in dom.walk():
        if  name == 'em': 
            # The Data class represents
            # the text inside the tags.

            x = Data('It is cool')

            # It appends x to em text.
            ind.append(x)
    
    print dom
    

Output.

    <body > <em > It is cool</em> </body>
    

How to add new html tags to the dom.
    from ehp import *
    
    html = Html()
    
    data = '''
    <body> <em> foo </em> </body>
    '''
    
    dom = html.feed(data)
    
    # The method sail_with_root
    # walks through the dom and gives you
    # the root tag for the tag in item.
    #
    # This is specially useful when you want
    # to delete/insert tags based on conditions.

    for root, item in dom.sail_with_root():
        # If it is an em tag then substitute it for
        # a paragraph tag.

        if item.name == 'em':
            root.remove(item)
            x = Tag('p')
            x.append(Data('foo'))
            root.append(x)
    
    print dom
    
Output.

    <body >  <p >foo</p></body>
    

Anoter example with tag attributes.
    from ehp import *
    
    data  = ''' <body><em> foo  </em></body>'''
    html  = Html()
    dom  = html.feed(data)
    
    
    for ind in dom.sail():
        if ind.name == 'body':
            x = Tag('font', {'color':'red'})
            ind.append(x)
    
    
    print dom
    
Output.
    <body ><em > foo  </em><font color="red" ></font></body>
    

Searching for tags.
    from ehp import *
    
    data = '''<html> <body> <em> Hello world. </em> </body> </html>'''
    
    html = Html()
    dom = html.feed(data)
    
    # The find method goes through all em tags.
    # The text method just prints the text inside a given tag.
    for ind in dom.find('em'):
        print ind.text()


Output.
    Hello world.

Other more complicated example.
    from ehp import *
    
    
    data = '''<html> <body> <em> Hello world. </em>  
              <em style="color:blue"> It is a python. </em> </body> </html>'''
    
    html = Html()
    dom = html.feed(data)
    
    for ind in dom.find('em'):
        print ind.text()
    
    # The first ocurrence of 'em'.
    print dom.fst('em').text()
    print dom.fst('body').text()
    print dom.fst('html').text()
    
    # This method returns the first ocurrence of a given tag
    # matching some attributes.
    root, item = dom.take_with_root(('style', 'color:blue'))
    print root
    print item
    
Output.
     It is a python. 
       Hello world. 
       Hello world.   
               It is a python.  
        Hello world.   
               It is a python.   
       <body  <em  Hello world. </em  
              <em style="color:blue"  It is a python. </em </body
     <em style="color:blue"  It is a python. </em
     
    

Other useful method find_with_root
    from ehp import *
    
    html = Html()
    dom = html.feed('''<body> <p> alpha </p> <p> beta </p> </body>''')
    
    for root, ind in dom.find_with_root('p'):
        root.remove(ind)
    
    print dom
    
Output.
    <body >   </body>

Delete tag attributes.
    from ehp import *
    
    html = Html()
    dom  = html.feed('''<body> <p style="color:black"> xxx </p> 
                     <p style = "color:black"> mmm </p></body>''')
    
    for root, ind in dom.match_with_root(('style', 'color:black')):
        del ind.attr['style']
    
    item = dom.fst('body')
    item.attr['style'] = 'color:black'
    
    print dom
    
Output.
    <body style="color:black" > <p > xxx </p> <p > mmm </p></body>


Going through tags that match some attribute condition.

    from ehp import *
    
    data = '''<html> <body> 
              <em style="background:blue"> It is a python. </em> 
              </body> </html>'''
    
    html = Html()
    dom = html.feed(data)
    
    for ind in dom.match(('style', 'background:blue')):
        print ind.text()
    
    
    for ind in dom.match(('style', 'background:blue'),
                          ('onclick', 'foo();')):
        # It shouldn't be printed.
        print ind.text()
    

Output.
    It is a python.


Some times you will need to insert tags after a given tag.

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

            # You have an insert_before method too.
            root.insert_after(ind, x)
    
    print tree
    
Output.
    <html >
        <body >
            <em > alpha </em><em ></em>
        </body>
    </html>


Matching ampersand.

    from ehp import *
    
    html = Html()
    data = '''<tag> The &amp; is a good &amp; symbol. </tag>'''
    dom = html.feed(data)
    
    for root, ind in dom.find_with_root(AMP):
        if ind.name == AMP:
            index = root.index(ind)
            root[index] = Data('ampersand')
    
    print dom
    

Output.

    <tag > The ampersand is a good ampersand symbol. </tag>
    
There are other methods defined in the classes, for documentation use help(Html)
help(Tag) etc.


Help
====
If you have sugestions or need help you can find me at irc.freenode.org
channel #vy.

You can contact me through email as well.
ioliveira@id.uff.br

I'm on facebook too.
https://www.facebook.com/iury.gomes.figueiredo

Old repository
==============
git clone ssh://olliveira@git.code.sf.net/p/easyhtmlparser/code easyhtmlparser-code

