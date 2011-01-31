import sys

LEFT = 0
RIGHT = 1
class binnode:
    def __init__(self, data):
        self.data = data
        self.children = [None,None]
    def __getitem__(self, side):
        return self.children[side]
    def __setitem__(self, side, data):
        self.children[side] = data
class bintree:
    def __init__(self, data):
        if type(data) != list:
            self.root = binnode(data)
        else:
            self.root = binnode(data[0])
            for xx in data[1:]:
                self.insert(xx)
    def insert(self, data):
        if type(data) != type(self.root.data):
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
                    curNode[side] = binnode(data)
                    inserted = True
                else:
                    curNode = curNode[side]
    def inorder(self, func):
        self.inorder_helper(func, self.root)
    def inorder_helper(self, func, node):
        if node[LEFT]:
            self.inorder_helper(func, node[LEFT])
        func(node.data)
        if node[RIGHT]:
            self.inorder_helper(func, node[RIGHT])
if __name__ == '__main__':
    foo = bintree(['foo', 'bar', 'fro', 'baz', 'zed'])
    print "An in order traversal of the tree:"
    foo.inorder(lambda(x): sys.stdout.write('%s\n'%x))
    try:
        foo.insert(1)
    except TypeError:
        print "Can't insert an int into a tree of strings."
