"""
    This program walks the directed graph of Wikipedia articles by following 
    internal hyperlinks, up to a certain maximum search depth from a given starting 
    node, and identifies cycles involving the start node.
    It shows how EHP is easy to use and parse big amount of data.
"""

import urllib2
import re
from ehp import *


class WikiGraph(object):
    def __init__(self, root, depth):
        self.root = root
        self.depth = depth
        """ it compiles a regex which characerizes a valid wiki link.
            like, it doesn't match links like /wiki/computer:top
            or things like /wiki/Main Page
        """
        self.hash_table = {}

        self.regexWiki = re.compile('/wiki/[^ ]+$')
        
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
        data = self.readUrl('http://en.wikipedia.org%s' % url) 
        links = self.filterLinks(data)
        return links

    def trackLinks(self, vertice, head, pointer, links, node):
        print 'trackLinks depth %s:%s' % (node, links)

        tmp = links[:]

        for ind in links:
            if ind == vertice:
                index = links.index(ind)
                del tmp[index]

                copy = pointer[:]
                copy.append(ind)
                head.append(copy)
                break


        if node >= self.depth:
            return

        
        for ind in tmp:
            pointer.append(ind)
           
            if self.hash_table.has_key(ind):
                self.trackLinks(vertice, head, pointer, self.hash_table[ind], node + 1)
            else:
                parsed = self.getLinks(ind)
                self.hash_table[ind] = parsed
                self.trackLinks(vertice, head, pointer, parsed, node + 1)

            pointer.pop()


    def analyze(self):
        #head = Graph(self.root)
        head = []
        pointer = [self.root]

        links = self.getLinks(self.root)

        self.trackLinks(self.root, head, pointer, links, 1)
        return head

"""here you pick up the depth and the article."""
if __name__ == '__main__':
    alpha = WikiGraph('/wiki/User:Joseph_Crowe/1', 100)
    #alpha = WikiGraph('/wiki/User:Joseph_Crowe/A', 10)
    head = alpha.analyze()

    print 'CYCLES:', str(head), len(head)



