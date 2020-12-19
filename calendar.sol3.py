# author: linnil1
# BSTree(Not balanced) -> cannot pass case2 only 
from enum import Enum

import sys
sys.setrecursionlimit(11000)


class NodeColor(Enum):
    RED = True
    BLACK = False


class Node:
    def __init__(self, key, value):
        # key, value
        self.key = key
        self.val = value

        # Tree attributes
        self.level = 1
        self.size = value
        self.color = NodeColor.RED

        # Silbiling
        self.left = None
        self.right = None

    def __lt__(self, x):
        """Comparison"""
        return self.key < x.key

    def __str__(self):
        """Formatter"""
        return f"<Node ({self.key},{self.val}) {self.level}"\
               f" {self.size} {self.color}>"

    def update(self):
        """Update size, level"""
        self.size = self.val
        if self.left is not None:
            self.size += self.left.size

        if self.right is not None:
            self.size += self.right.size

    def flipColor(self):
        # self.color = not self.color
        if self.color == NodeColor.RED:
            self.color = NodeColor.BLACK
        elif self.color == NodeColor.BLACK:
            self.color = NodeColor.RED


class RBTree:
    def __init__(self):
        self.root = None

    def size(self, r):
        if r is None:
            return 0
        else:
            return r.size

    def insNode(self, r, x):
        """Insert Node x to tree r"""
        if r is None:
            return x
        if x < r:
            r.left = self.insNode(r.left, x)
        elif r < x:
            r.right = self.insNode(r.right, x)
        else:
            r.val += x.val
            # raise ValueError("Same key in RBTree")

        r.update()
        return r

    def insert(self, key, value=None):
        """Insert the key,value to tree"""
        if value is None:
            value = key
        self.root = self.insNode(self.root, Node(key, value))
        self.root.color = NodeColor.BLACK

    def getNode(self, r, x):
        """Find Node x in tree r"""
        if r is None:
            return None

        if x < r:
            return self.getNode(r.left, x)
        elif r < x:
            return self.getNode(r.right, x)
        else:
            return r.val

    def get(self, key):
        """Find the value of the key in the tree"""
        return self.getNode(self.root, Node(key, None))

    def indNode(self, r, i):
        """Find the index of keys"""
        if r is None:
            raise ValueError("Not such index")
        if i < self.size(r.left):
            return self.indNode(r.left, i)
        i -= self.size(r.left)
        if i < r.val:
            return r
        return self.indNode(r.right, i - r.val)

    def index(self, i):
        """Find the index of keys"""
        return self.indNode(self.root, i).key

    def lrNode(self, r, x, include):
        if r is None:
            return 0
        if x < r:
            return self.lrNode(r.left, x, include)
        elif r < x:
            return self.size(r.left) + r.val + self.lrNode(r.right, x, include)
        else:
            s = self.size(r.left)
            if include:
                s += r.val
            return s

    def floor(self, key):
        """Find the floor index of keys"""
        return self.lrNode(self.root, Node(key, None), False)

    def ceil(self, key):
        """Find the floor index of keys"""
        return self.lrNode(self.root, Node(key, None), True)

    def iterTree(self, r):
        if r is None:
            return
        t = 2 * r.level - 2
        if not self.isRed(r):
            t += 1
        self.iterTree(r.left)
        print(" " * t + str(r), r.left, r.right)
        self.iterTree(r.right)

    def print(self):
        print("---")
        self.iterTree(self.root)
        print("---")

    def checkNode(self, r):
        if r is None:
            return True
        if not self.checkNode(r.left):
            return False
        if not self.checkNode(r.right):
            return False

        # color
        if self.isRed(r.right):
            print('1')
            return False
        if self.isRed(r.left) and self.isRed(r.left.left):
            print('2')
            return False

        # size and level
        if r.size != 1 + self.size(r.left) + self.size(r.right):
            print('3')
            return False
        if r.level != self.level(r.right) + 1:
            print('4')
            return False
        if self.isRed(r.left) and r.level != self.level(r.left):
            print('5')
            return False
        if not self.isRed(r.left) and r.level != self.level(r.left) + 1:
            print('6')
            return False
        return True

    def check(self):
        return self.checkNode(self.root)


class Calendar:
    def __init__(self):
        self.tree = RBTree()

    def book(self, start: int, end: int) -> bool:
        assert start < end
        a = self.tree.ceil(start)
        b = self.tree.floor(end)
        # print(start, end, a, b)
        if a % 2 or a != b:
            return False

        self.tree.insert(start, 1)
        self.tree.insert(end, 1)
        return True


if __name__ == "__main__":
    a = Calendar()
    print(a.book(10, 20))
    print(a.book(15, 25))
    print(a.book(20, 25))
    print(a.book(17, 21))
    print(a.book(0, 3))
    print(a.book(2, 6))
    print(a.book(3, 6))
    """
    True
    False
    True
    False
    True
    False
    True
    """

    a = Calendar()
    print(a.book(5, 15))
    print(a.book(0, 18))
    print(a.book(24, 29))
    print(a.book(13, 25))
    print(a.book(18, 22))
    print(a.book(15, 18))
    """
    True
    False
    True
    False
    True
    True
    """
