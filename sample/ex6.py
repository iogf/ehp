"""
    This program walks the directed graph of Wikipedia articles by following 
    internal hyperlinks, up to a certain maximum search depth from a given starting 
    node, and identifies cycles involving the start node.
    It shows how EHP is easy to use and parse big amount of data.
"""

import urllib2
import re
from ehp import *
count = 0

class Graph(object):
    def __init__(self, vertice):
        self.vertice = vertice
        self.down = []

    def __str__(self):
        data = '%s' % self.vertice

        for ind in self.down:
            data += '\n---%s->%s\n' % (str(self.vertice), str(ind))


        data += '\n'
        return data

    def getCycle(self):
        path = [self.vertice]

        for ind in self.down:
            way = ind.hasPath(self.vertice)

            if way:
                path.append(way)

        return path


    def hasPath(self, vertice):
        path = False
        if self.vertice == vertice:
            global count
            count += 1
            return [self.vertice]

        for ind in self.down:
            way = ind.hasPath(vertice)

            if way:
                if not path:
                    path = [self.vertice]

                path.append(way)

        return path

class WikiGraph(object):
    def __init__(self, root, depth):
        self.root = root
        self.depth = depth
        """ it compiles a regex which characerizes a valid wiki link.
            like, it doesn't match links like /wiki/computer:top
            or things like /wiki/Main Page
        """

        self.regexWiki = re.compile('/wiki/[^ ]+$')
        self.graph = Graph(root)
        self.count = 0
        self.hash_table = {}

        """ get the root article set the depth. """
            
    def readUrl(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        layout = opener.open(url).read()

        return layout

    def isWikiLink(self, link):
        match = re.match(self.regexWiki, link)

        return match

    def filterLinks(self, data):
        x = Html()

        tree = x.feed(data)

        """the step 1 filters all the tags which start with p or ul(unordered list)
           since all content on wiki are inside those two kind of tags.
        """

        step1 = [ind for ind in tree.sail()
                        if ind.name == 'div'
                            if ind.attr['id'] == 'bodyContent']

        bodyContent = step1[0]

        step2 = [ind for ind in bodyContent.sail()
                        if ind.name == 'p' or ind.name == 'ul']


        step3 = [indj for indi in step2
                        for indj in indi.sail()
                            if indj.name == 'a']


        step4 = [ind for ind in step3
                            if self.isWikiLink(ind.attr['href'])]


    
        step5 = [ind.attr['href'] for ind in step4]                    

        return step5

    def getLinks(self, url):
        print url
        data = self.readUrl('http://en.wikipedia.org%s' % url) 
        links = self.filterLinks(data)
        return links

    def trackLinks(self, head, links, node):
        print 'trackLinks depth %s:%s' % (node, links)

        for ind in links:
            current = Graph(ind)
            head.down.append(current)
           
            if node < self.depth:
                if self.hash_table.has_key(ind):
                    self.trackLinks(current, self.hash_table[ind], node + 1)
                else:
                    parsed = self.getLinks(ind)
                    self.hash_table[ind] = parsed
                    self.trackLinks(current, parsed, node + 1)



    def analyze(self):
        head = Graph(self.root)
        links = self.getLinks(self.root)
        self.hash_table[self.root] = links
        self.trackLinks(head, links, 1)
        return head

if __name__ == '__main__':
    alpha = WikiGraph('/wiki/User:Joseph_Crowe/A', 10)
    head = alpha.analyze()

    #print 'REPRESENTATION:', str(head)
    print 'Cycles:', head.getCycle()
    print count


""" result:
    trackLinks depth 10:['/wiki/User:Joseph_Crowe/H', '/wiki/User:Joseph_Crowe/D']
Cycles: ['/wiki/User:Joseph_Crowe/A', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/G', ['/wiki/User:Joseph_Crowe/F', ['/wiki/User:Joseph_Crowe/E', ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]]]], ['/wiki/User:Joseph_Crowe/G', ['/wiki/User:Joseph_Crowe/F', ['/wiki/User:Joseph_Crowe/G', ['/wiki/User:Joseph_Crowe/F', ['/wiki/User:Joseph_Crowe/E', ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]], ['/wiki/User:Joseph_Crowe/E', ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A'], ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]], ['/wiki/User:Joseph_Crowe/J', ['/wiki/User:Joseph_Crowe/H', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]], ['/wiki/User:Joseph_Crowe/D', ['/wiki/User:Joseph_Crowe/C', ['/wiki/User:Joseph_Crowe/B', ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]], ['/wiki/User:Joseph_Crowe/I', ['/wiki/User:Joseph_Crowe/A']]]]]]]]]]
95
tau@spin:~/lib/code/python/html/sample/ex6$ 
"""


