import bintree
from bintree import LEFT, RIGHT

class rbnode(bintree.binnode):
    def __init__(self, data):
        bintree.binnode.__init__(self, data)
        self.isRed = True
    def getGrandparent(self):
        if self.parent != None:
            return self.parent
        else:
            return None
    def getUncle(self):
        grand = self.getGrandparent()
        uncle = None
        if grand != None:
            if grand[LEFT] == self.parent:
                uncle = grand[RIGHT]
            else:
                uncle = grand[LEFT]
        return uncle

class rbtree(bintree.bintree):
    def __init__(self, data):
        bintree.bintree.__init__(self, data, rbnode)
    def insert(self, data):
        newnode = bintree.bintree.insert(self, data)
        self.insertcleanup(newnode)
        return newnode
    def insertcleanup(self, node):
        pass
    def rotateright(self, node):
        return self.rotatenode(node, LEFT, RIGHT)
    def rotateleft(self, node):
        return self.rotatenode(node, RIGHT, LEFT)
    def rotatenode(self, node, rotside, fixside):
        if node:
            parent = node
            grandparent = node.parent
            rotchild = node[rotside] #child which is rotating
            if rotchild:
                if grandparent:
                    if grandparent[rotside] == parent:
                        grandparent[rotside] = rotchild
                    else:
                        grandparent[fixside] = rotchild
                rotchild.parent = grandparent
                node[rotside] = rotchild[fixside]
                if node[rotside]:
                    node[rotside].parent = node
                rotchild[fixside] = node
                node.parent = rotchild
                if rotchild.parent == None:
                    self.root = rotchild
