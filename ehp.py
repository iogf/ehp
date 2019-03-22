from html.parser import HTMLParser
from collections import deque

version = '1.3'
DATA    = 1
META    = 2
COMMENT = 3
PI      = 4
CODE    = 5
AMP     = 6

class Attribute(dict):
    """ 
    This class holds the tags's attributes.
    The idea consists in providing an efficient and flexible way of manipulating
    tags attributes inside the dom.

    Example:
    dom = Html().feed('<p style="color:green"> foo </p>')

    for ind in dom.sail():
        if ind.name == 'p':
            ind.attr['style'] = "color:blue"

    It would change to color blue.
    """

    def __getitem__(self, key):
        """ 
        If self doesn't have the key it returns '' 
        """

        return self.get(key, '')

    def __str__(self):
        """ 
        It returns a htmlized representation for attributes 
        which are inside self.
        """

        data = ''
        for key, value in list(self.items()):
            pair = '%s="%s" ' % (key, value)
            data = data + pair

        return data


class Root(list):
    """ 
    A Root instance is the outmost node for a xml/html document.
    All xml/html entities inherit from this class.

    html = Html()    
    dom = html.feed('<html> ... </body>')

    dom.name == ''
    True
    type(dom) == Root
    True

    """


    def __init__(self, name=None, attr={}):
        """
        """

        self.name = name
        self.attr = Attribute(attr)

        list.__init__(self)

    __repr__ = object.__repr__

    def __str__(self):
        """ 
        This str function returns a string representation of the structure.
        """

        html = ''

        for ind in self:
            html = '%s%s' % (html, ind)

        return html

    def sail(self):
        """ 
        This is used to navigate through the xml/html document.
        Every xml/html object is represented by a python class
        instance that inherits from Root.
        
        The method sail is used to return an iterator
        for these objects.

        Example:
        data = '<a> <b> </b> </a>'

        html = Html()
        dom = html.feed(data)

        for ind in dom.sail():
            print type(ind),',', ind.name

        It would output.

        <class 'ehp.Root'> , a
        <class 'ehp.Root'> , b
        """
           
        for indi in self[:]:
            for indj in indi.sail():
                yield(indj)

            yield(indi)

    def index(self, item):
        """
        This is similar to index but uses id
        to check for equality.

        Example:

        data = '<a><b></b><b></b></a>'
        html = Html()
        dom = html.feed(data)
        
        for root, ind in dom.sail_with_root():
            print root.name, ind.name, root.index(ind)


        It would print.

        a b 0
        a b 1
         a 0        

        The line where it appears ' a 0' corresponds to the
        outmost object. The outmost object is an instance of Root
        that contains all the other objects.
        """

        count = 0
        for ind in self:
            if ind is item: return count
            count = count + 1

        raise ValueError

    def remove(self, item):
        """
        This is as list.remove but works with id.

        data = '<a><b></b><b></b></a>'
        html = Html()
        dom = html.feed(data)
        
        for root, ind in dom.sail_with_root():
            if ind.name == 'b':
                root.remove(ind)
        
        print dom
        
        It should print.

        <a ></a>
        """

        index = self.index(item)
        del self[index]

    def find(self, name, *args):
        """
        It is used to find all objects that match name.

        Example 1:

        data = '<a><b></b><b></b></a>'
        html = Html()
        dom = html.feed(data)

        for ind in dom.find('b'):
            print ind

        It should print.

        <b ></b>
        <b ></b>

        Example 2.

        data = '<body> <p> alpha. </p> <p style="color:green"> beta.</p> </body>'
        html = Html()
        dom  = html.feed(data)
        
        for ind in dom.find('p', ('style', 'color:green')):
            print ind
        
        Output.
    
        
        <p style="color:green" > beta.</p>
        """

        for ind in self.sail():
            if ind.name == name:
                for key, value in args:
                    if ind.attr[key] != value:
                        break
                else:
                    yield(ind)

    def find_with_root(self, name, *args):
        """
        Like Root.find but returns its parent tag.

        from ehp import *
        
        html = Html()
        dom = html.feed('''<body> <p> alpha </p> <p> beta </p> </body>''')
        
        for root, ind in dom.find_with_root('p'):
            root.remove(ind)
        
        print dom

        It would output.

        <body >   </body>        
        """

        for root, ind in self.sail_with_root():
            if ind.name == name:
                for key, value in args:
                    if ind.attr[key] != value:
                        break
                else:
                    yield(root, ind)


    def byid(self, id):
        """
        It is a shortcut for finding an object
        whose attribute 'id' matches id.

        Example:

        data = '<a><b id="foo"></b></a>'
        html = Html()
        dom = html.feed(data)
        
        print dom.byid('foo')
        print dom.byid('bar')

        It should print.

        <b id="foo" ></b>
        None
        """
    
        return self.take(('id', id))

    def take(self, *args):
        """
        It returns the first object whose one of its
        attributes matches (key0, value0), (key1, value1), ... .

        Example:

        data = '<a><b id="foo" size="1"></b></a>'
        html = Html()
        dom = html.feed(data)
        
        print dom.take(('id', 'foo'))
        print dom.take(('id', 'foo'), ('size', '2'))
        """

        seq = self.match(*args)
        
        try:
            item = next(seq)
        except StopIteration:
            return None
        else:
            return item

    def take_with_root(self, *args):
        """
        Like Root.take but returns the tag parent.
        """

        seq = self.match_with_root(*args)
        
        try:
            item = next(seq)
        except StopIteration:
            return None
        else:
            return item


        pass

    def match(self, *args):
        """
        It returns a sequence of objects whose attributes match.
        (key0, value0), (key1, value1), ... .

        Example:

        data = '<a size="1"><b size="1"></b></a>'
        html = Html()
        dom = html.feed(data)
        
        for ind in dom.match(('size', '1')):
            print ind

        It would print.

        <b size="1" ></b>
        <a size="1" ><b size="1" ></b></a>
        """

        for ind in self.sail():
            for key, value in args:
                if ind.attr[key] != value: 
                    break
            else: 
                yield(ind)

    def match_with_root(self, *args):
        """
        Like Root.match but with its parent tag.

        Example:

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

        <body style="color:black" > <p > xxx </p> 
                         <p > mmm </p></body>
        """

        for root, ind in self.sail_with_root():
            for key, value in args:
                if ind.attr[key] != value: 
                    break
            else: 
                yield(root, ind)


    def join(self, delim, *args):
        """
        It joins all the objects whose name appears in args.

        Example 1:

        html = Html()
        data = '<a><b> This is cool. </b><b> That is. </b></a>'
        dom = html.feed(data)
        
        print dom.join('', 'b')
        print type(dom.join('b'))

        It would print.

        <b > This is cool. </b><b > That is. </b>
        <type 'str'>

        Example 2:

        html = Html()
        data = '<a><b> alpha</b><c>beta</c> <b>gamma</a>'
        dom = html.feed(data)
        
        print dom.join('', 'b', 'c')

        It would print.

        <b > alpha</b><c >beta</c><b >gamma</b>

        Example 3:


        html = Html()
        data = '<a><b>alpha</b><c>beta</c><b>gamma</a>'
        dom = html.feed(data)
        
        print dom.join('\n', DATA)

        It would print.

        alpha
        beta
        gamma
        """

        data = ''

        for ind in self.sail():
            if ind.name in args:
                data = '%s%s%s' % (data, delim, ind)

        return data

    def fst(self, name, *args):
        """
        It returns the first object whose name
        matches.

        Example 1:

        html = Html()
        data = '<body> <em> Cool. </em></body>'
        dom = html.feed(data)
        
        print dom.fst('em')

        It outputs.

        <em > Cool. </em>

        Example 2:

        data = '<body> <p> alpha. </p> <p style="color:green"> beta.</p> </body>'
        html = Html()
        dom  = html.feed(data)
        
        for ind in dom.find('p', ('style', 'color:green')):
            print ind
        
        print dom.fst('p', ('style', 'color:green'))
        print dom.fst_with_root('p', ('style', 'color:green'))

        Output:

        <p style="color:green" > beta.</p>
        <p style="color:green" > beta.</p>
        (<ehp.Tag object at 0xb7216c0c>, <ehp.Tag object at 0xb7216d24>)
        """

        
        # for ind in self.sail():
        #    if ind.name == name:
        #        for key, value in args:
        #            if ind.attr[key] != value:
        #                break
        #        else:
        #            return ind

        seq = self.find(name, *args)

        try:
            item = next(seq)
        except StopIteration:
            return None
        else:
            return item

    def fst_with_root(self, name, *args):
        """
        Like fst but returns its item parent.

        Example:

        html = Html()
        data = '<body> <em> Cool. </em></body>'
        dom = html.feed(data)
        
        root, item dom.fst_with_root('em')
        root.insert_after(item, Tag('p'))
        print root

        It outputs.

        <body > <em > Cool. </em><p ></p></body>

        For another similar example, see help(Root.fst)
        """

        # for root, ind in self.sail_with_root():
        #    if ind.name == name:
        #        for key, value in args:
        #            if ind.attr[key] != value:
        #                break
        #        else:
        #            return root, ind
        
        seq = self.find_with_root(name, *args)

        try:
            item = next(seq)
        except StopIteration:
            return None
        else:
            return item


    def text(self):
        """
        It returns all objects whose name matches DATA.
        It basically returns a string corresponding
        to all asci characters that are inside a xml/html
        tag.


        Example:

        html = Html()
        data = '<body><em>This is all the text.</em></body>'
        dom = html.feed(data)
        
        print dom.fst('em').text()

        It outputs.

        This is all the text.

        Notice that if you call text() on an item with
        children then it returns all the *printable* characters
        for that node.
        """

        return self.join('', DATA, AMP, CODE)


    def write(self, filename):
        """
        It saves the structure to a file.
        """

        fd = open(filename, 'w')
        fd.write(self)
        fd.close()


    def sail_with_root(self):
        """ 
        This one works like sail(), however it yields the tag's parents as
        well as the child tag.
        
        For an example, see help(Root.remove).
        """

        for indi in self[:]:
            for indj in indi.sail_with_root():
                yield(indj)

            yield((self, indi))

    def walk(self):
        """
        Like sail but carries name and attr.

        Example:

        html = Html()
        data = '<body> <em> This is all the text.</em></body>'
        dom = html.feed(data)
        
        for ind, name, attr in dom.walk():
            print 'TAG:', ind
            print 'NAME:', name
            print 'ATTR:', attr

        It should print.

        TAG:  
        NAME: 1
        ATTR: 
        TAG:  This is all the text.
        NAME: 1
        ATTR: 
        TAG: <em > This is all the text.</em>
        NAME: em
        ATTR: 
        TAG: <body > <em > This is all the text.</em></body>
        NAME: body
        ATTR: 
        """

        for ind in self.sail():
            yield (ind, ind.name, ind.attr)

    def walk_with_root(self):
        """
        Like walk but carries root.

        Example:

        html = Html()
        data = '<body><em>alpha</em></body>'
        dom = html.feed(data)
        
        for (root, name, attr), (ind, name, attr) in dom.walk_with_root():
            print root, name, ind, name

        Output:

        <em >alpha</em> 1 alpha 1
        <body ><em >alpha</em></body> em <em >alpha</em> em
        <body ><em >alpha</em></body> body <body ><em >alpha</em></body> body    
        """

        for root, ind in self.sail_with_root():
            yield ((root, root.name, root.attr), 
                   (ind, ind.name, ind.attr))

    def insert_after(self, y, k):
        """ 
        Insert after a given tag. 

        For an example, see help(Root.fst_with_root).
        """

        ind = self.index(y)
        self.insert(ind + 1, k)

    def insert_before(self, y, k):
        """ 
        Insert before a given tag. 

        For a similar example, see help(Root.fst_with_root).
        """

        ind = self.index(y)
        self.insert(ind, k)


class Tag(Root):
    """ 
    This class's instances represent xml/html tags under the form:
    <name key="value" ...> ... </name>.

    It holds useful methods for parsing xml/html documents.

    """

    def __init__(self, name, attr={}):
        """
        The parameter name is the xml/html tag's name.

        Example:

        d = {'style': 'background:blue;'}
        x = Tag('p', d)
        """
        Root.__init__(self, name, attr)

    def __str__(self):
        """ 
        This function returns a string representation for a node.
        """

        html = '<%s %s>' % (self.name, self.attr)
   

        for ind in self:
            html = '%s%s' % (html, ind)

        html = html + '</%s>' % self.name

        return html


class Data(Root):
    """ 
    The pythonic representation of data that is inside xml/html documents.

    All data that is not a xml/html token is represented by this class in the
    structure of the document.

    Example:

    html = Html()
    data = '<body><em>alpha</em></body>'
    dom = html.feed(data)
        
    x = dom.fst('em')
    
    # x holds a Data instance.

    type(x[0])        
    print x[0]

    Output:

    <class 'ehp.Data'>
    alpha
    
    The Data instances are everywhere in the document, when
    the tokenizer finds them between the xml/html tags it builds
    up the structure identically to the document.
    """

    def __init__(self, data):
        """
        The data holds the characters.

        Example:

        html = Html()
        data = '<body><em>alpha</em></body>'
        dom = html.feed(data)
        x = dom.fst('em')
        x.append(Data('\nbeta'))

        It outputs.

        <body ><em >alpha
        beta</em></body>
        """

        Root.__init__(self, DATA)
        self.data = data

    def __str__(self):
        """ 
        This function returns a string which correspond to the data inside the
        Data class.
        """

        return self.data

    def text(self):
        return self.data

class XTag(Root):
    """ 
    This tag is the representation of html's tags in XHTML style like <img src="t.gif" />
    It is tags which do not have children.

    """

    def __init__(self, name, attr={}):
        """
        See help(Tag).
        """
        Root.__init__(self, name, attr)


    def __str__(self):
        html = '<%s %s/>' % (self.name, self.attr)

        return html


class Meta(Root):
    """ 

    """

    def __init__(self, data):
        Root.__init__(self, META)
        self.data = data

    def __str__(self):
        html = '<!%s>' % self.data

        return html

class Code(Root):
    """ 
    """

    def __init__(self, data):
        Root.__init__(self, CODE)
        self.data = data

    def __str__(self):
        html = '&#%s' % self.data

        return html

class Amp(Root):
    """ 

    """

    def __init__(self, data):
        Root.__init__(self, AMP)
        self.data = data

    def __str__(self):
        html = '&%s' % self.data

        return html


class Pi(Root):
    """

    """

    def __init__(self, data):
        Root.__init__(self, PI)
        self.data = data

    def __str__(self):
        html = '<?%s>' % self.data

        return html


class Comment(Root):
    """

    """

    def __init__(self, data):
        Root.__init__(self, COMMENT)
        self.data = data

    def __str__(self):
        html = '<!--%s-->' % self.data

        return html


class Tree(object):
    """ 
    The engine class.
    """

    def __init__(self):
        """
        Initializes outmost which is the struct which will 
        hold all data inside the file.
        """

        self.outmost = Root('')

        self.stack = deque()
        self.stack.append(self.outmost)

    def clear(self):
        """ 
        Clear the outmost and stack for a new parsing. 
        """

        self.outmost = Root('')
        self.stack.clear()
        self.stack.append(self.outmost)

    def last(self):
        """ 
        Return the last pointer which point to the actual tag scope.
        """

        return self.stack[-1]

    def nest(self, name, attr):
        """
        Nest a given tag at the bottom of the tree using 
        the last stack's pointer.
        """

        item = Tag(name, attr)

        pointer = self.stack.pop()

        pointer.append(item)

        self.stack.append(pointer)

        self.stack.append(item)

    def dnest(self, data):
        """ 
        Nest the actual data onto the tree. 
        """

        top = self.last()

        item = Data(data)

        top.append(item)

    def xnest(self, name, attr):
        """ 
        Nest a XTag onto the tree. 
        """

        top = self.last()

        item = XTag(name, attr)

        top.append(item)


    def ynest(self, data):
        """

        """

        top = self.last()

        item = Meta(data)

        top.append(item)


    def mnest(self, data):
        """

        """

        top = self.last()

        item = Comment(data)

        top.append(item)

    def cnest(self, data):
        """

        """

        top = self.last()

        item = Code(data)

        top.append(item)


    def rnest(self, data):
        """

        """

        top = self.last()

        item = Amp(data)

        top.append(item)


    def inest(self, data):
        """

        """

        top = self.last()

        item = Pi(data)

        top.append(item)

    def enclose(self, name):
        """ 
        When found a closing tag then pops the pointer's scope from the stack
        so pointing to the earlier scope's tag.
        """

        count = 0

        for ind in reversed(self.stack):
            count = count + 1

            if ind.name == name:
                break
        else:
            count = 0

        # It pops all the items which do not match with the closing tag.
        for i in range(0, count):
            self.stack.pop()


class Html(HTMLParser):
    """ 
    The tokenizer class.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.struct = Tree()

    def fromfile(self, filename):
        """
        It builds a structure from a file.
        """

        fd   = open(filename, 'r')
        data = fd.read()
        fd.close()
        return self.feed(data)

    def feed(self, data):
        """

        """

        self.struct.clear()
        HTMLParser.feed(self, data)

        return self.struct.outmost

    def handle_starttag(self, name, attr):
        """ 
        When found an opening tag then nest it onto the tree 
        """

        self.struct.nest(name, attr)
        pass

    def handle_startendtag(self, name, attr):
        """ 
        When found a XHTML tag style then nest it up to the tree
        """

        self.struct.xnest(name, attr)

    def handle_endtag(self, name):
        """ 
        When found a closing tag then makes it point to the right scope 
        """

        self.struct.enclose(name)
        pass

    def handle_data(self, data):
        """ 
        Nest data onto the tree. 
        """

        self.struct.dnest(data)    

    def handle_decl(self, decl):
        """

        """
        self.struct.ynest(decl)

    def unknown_decl(self, decl):
        """

        """
        self.struct.ynest(decl)

    def handle_charref(self, data):
        """

        """

        self.struct.cnest(data)

    def handle_entityref(self, data):
        """

        """

        self.struct.rnest(data)

    def handle_pi(self, data):
        """
        """

        self.struct.inest(data)

    def handle_comment(self, data):
        """

        """

        self.struct.mnest(data)



























