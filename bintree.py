# Sorted Binary Tree library
# For usage, take a look at the example code in the main section.
import sys

LEFT = 0
RIGHT = 1
class binnode:
    """
    Object representing a single node in a binary tree.

    self.data: The data associated with this node
    self.children: Child nodes of this node. Children can be accessed
      by self[LEFT] and self[RIGHT]
    """
    def __init__(self, data):
        self.data = data
        self.children = [None,None]
        self.parent = None
    def __getitem__(self, side):
        return self.children[side]
    def __setitem__(self, side, data):
        self.children[side] = data
class bintree:
    """
    Object representing a sorted binary tree.

    self.root: The tree's root node.
    init takes either a single data point, or an array. If an array,
      all items must be of the same type, otherwise a TypeError
      exception will be raised. Optionally, the nodetype argument can
      specify a subclass of binnode to use for all node instantiations.
    insert: Inserts a new node into the tree at the appropriate point,
      with a payload of 'data'. Will raise a TypeError if the type of
      'data' is different then that of the root node, unless both are
      numbers.
    inorder: Performs an inorder traversal of the tree's nodes, applying
      'func' to the data of each.

    Exceptions: TypeError
    """
    def __init__(self, data, nodetype=binnode):
        self.root = None
        if issubclass(nodetype, binnode):
            self.nodetype = nodetype
            if type(data) != list:
                insert(data)
            else:
                for xx in data:
                    self.insert(xx)
        else:
            raise TypeError("nodetype must derive from binnode")
    def insert(self, data):
        newnode = self.nodetype(data)
        if self.root:
            if type(data) != type(self.root.data) and not (hasattr(data, '__int__') and hasattr(self.root.data, '__int__')):
                raise TypeError('Mismatch between inserted type (%s) and type of root (%s)' % (type(data).__name__, type(self.root.data).__name__))
            else:
                curNode = self.root
                inserted = False
                while not inserted:
                    if data < curNode.data:
                        side = LEFT
                    else:
                        side = RIGHT
                    if curNode[side] == None:
                        curNode[side] = newnode
                        newnode.parent = curNode
                        inserted = True
                    else:
                        curNode = curNode[side]
        else:
            self.root = newnode
        return newnode
    def inorder(self, func):
        self.inorder_helper(func, self.root)
    def inorder_helper(self, func, node):
        if node[LEFT]:
            self.inorder_helper(func, node[LEFT])
        func(node.data)
        if node[RIGHT]:
            self.inorder_helper(func, node[RIGHT])
    def getnode(self, data):
        curnode = self.root
        searching = True
        while searching:
            if curnode == None:
                searching = False
            elif curnode.data == data:
                searching = False
            elif curnode.data > data:
                curnode = curnode[LEFT]
            else:
                curnode = curnode[RIGHT]
        return curnode
if __name__ == '__main__':
    testsets = [ [['foo', 'bar', 'fro', 'baz', 'zed'], 1],
                 [[2, 1, 1.5, -3.0, 4.123456598, -9999999], 'asdf']]
    print "Running test sets:"
    for test in testsets:
        print ""
        atree = bintree(test[0])
        print "An in order traversal of the tree:"
        atree.inorder(lambda(x): sys.stdout.write('%s\n'%x))
        try:
            atree.insert(test[1])
        except TypeError:
            print "ERROR: Can't insert type %s into this list" % type(test[1]).__name__
