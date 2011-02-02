import bintree
from bintree import LEFT, RIGHT

# set debug to True if you want to see which cases are executed
# during inserts.
debug = False
def DebugPrint(string):
    if debug:
        print string

class rbnode(bintree.binnode):
    def __init__(self, data):
        bintree.binnode.__init__(self, data)
        self.isRed = True
    def getGrandparent(self):
        if self.parent != None:
            return self.parent.parent
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
        if not node:
            pass
        elif node.parent == None:
            DebugPrint('Case 1: %s' % node.data)
            node.isRed = False
        else:
            self.cleanup_case2(node)
    def cleanup_case2(self, node):
        if not node.parent.isRed:
            DebugPrint('Case 2: %s' % node.data)
        else:
            self.cleanup_case3(node)
    def cleanup_case3(self, node):
        uncle = node.getUncle()
        if uncle and uncle.isRed:
            DebugPrint('Case 3: %s, Uncle is %s' % (node.data, uncle.data))
            node.parent.isRed = False
            uncle.isRed = False
            grandparent = node.getGrandparent()
            grandparent.isRed = True
            self.insertcleanup(grandparent)
        else:
            self.cleanup_case4(node)
    def cleanup_case4(self, node):
        grandparent = node.getGrandparent()
        if node == node.parent[RIGHT] and node.parent == grandparent[LEFT]:
            DebugPrint('Case 4 (RIGHT): %s' % node.data)
            self.rotateleft(node.parent)
            node = node[LEFT]
        elif node == node.parent[LEFT] and node.parent == grandparent[RIGHT]:
            DebugPrint('Case 4 (LEFT): %s' % node.data)
            self.rotateright(node.parent)
            node = node[RIGHT]
        self.cleanup_case5(node)
    def cleanup_case5(self, node):
        DebugPrint('Case 5: %s' % node.data)
        grandparent = node.getGrandparent()
        node.parent.isRed = False
        grandparent.isRed = True
        if node == node.parent[LEFT]:
            self.rotateright(grandparent)
        else:
            self.rotateleft(grandparent)
    def rotateright(self, node):
        return self.rotatenode(node, LEFT, RIGHT)
    def rotateleft(self, node):
        return self.rotatenode(node, RIGHT, LEFT)
    def rotatenode(self, node, rotside, fixside):
        if node:
            parent = node.parent
            rotchild = node[rotside] #child which is rotating
            if rotchild:
                if parent:
                    if parent[LEFT] == node:
                        parent[LEFT] = rotchild
                    else:
                        parent[RIGHT] = rotchild
                rotchild.parent = parent
                node[rotside] = rotchild[fixside]
                if node[rotside]:
                    node[rotside].parent = node
                rotchild[fixside] = node
                node.parent = rotchild
                if rotchild.parent == None:
                    self.root = rotchild
    def isNodeRed(self, node):
        if node:
            return node.isRed
        else:
            return False

def runtest(testname, observed, expected, errorstring):
    print "Running test: %s" % testname
    print '\tExpected: %s' % expected
    print '\tObserved: %s' % observed
    if observed == expected:
        print "\tPASS"
    else:
        print "\tFAIL: %s" % errorstring
        raise AssertionError(errorstring)

def checknode(testname, node, value, isRed):
    runtest("%s Value" % testname, node.data, value, "Unexpected Value!")
    runtest("%s Color" % testname, node.isRed, isRed, "Unexpected Value!")

if __name__ == '__main__':
    # Generate a known tree, and check that nodes are as expected
    debug = True
    atree = rbtree([5, 2, 7, -4, 27, 8, 6, 19])
    checknode("Root", atree.root, 5, False)
    checknode("Node 2", atree.root[LEFT], 2, False)
    checknode("Node 3", atree.root[LEFT][LEFT], -4, True)
    checknode("Node 4", atree.root[RIGHT], 8, True)
    checknode("Node 5", atree.root[RIGHT][LEFT],  7, False)
    checknode("Node 6", atree.root[RIGHT][LEFT][LEFT], 6, True)
    checknode("Node 7", atree.root[RIGHT][RIGHT], 27, False)
    checknode("Node 8", atree.root[RIGHT][RIGHT][LEFT], 19, True)
    runtest("getnode1", atree.getnode(27), atree.root[RIGHT][RIGHT], "Unexpected node returned by atree.getnode(27)")
    newnode = atree.insert(10)
    checknode("Insert1", atree.root[RIGHT][RIGHT][LEFT], 10, True)
    checknode("Insert2", atree.root[RIGHT][RIGHT], 19, False)
    checknode("Insert3", atree.root[RIGHT][RIGHT][RIGHT], 27, True)
    runtest("Insert4", atree.getnode(10), newnode, "Unexpected value returned by atree.getnode(10)")
