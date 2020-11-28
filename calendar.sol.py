# author: linnil1
# Segment Tree

class Node:
    def __init__(self, a, b):
        self.left = None
        self.right = None
        self.status = 'o'
        self.start = a
        self.end = b


class Calendar:
    def __init__(self):
        # time_max = 1000000001
        time_max = 1000001
        self.root = Node(0, time_max)

    def addNode(self, r, a, b):
        # print(r.start, r.end, a, b)
        assert a < b
        assert r.start <= a
        assert b <= r.end 
        assert r.start < r.end
        assert r.status != 'x'

        if r.start == a and r.end == b:
            r.status = 'x'
            return

        if r.status == 'o':
            sep = (r.start + r.end) // 2
            r.left = Node(r.start, sep)
            r.right = Node(sep, r.end)
        else:
            sep = r.right.start

        r.status = '-'
        if a < sep:
            self.addNode(r.left, a, min(b, sep))
        if b > sep:
            self.addNode(r.right, max(a, sep), b)

        if r.left.status == 'x' and r.right.status == 'x':
            r.status = 'x'

    def isUsedNode(self, r, a, b):
        # print(r.start, r.end, a, b)
        assert a < b
        assert r.start <= a
        assert b <= r.end 
        assert r.start < r.end

        # status is o and x when size = 1
        # status is o and x in leaf

        if r.status == 'o':
            return False
        if r.status == 'x':
            return True

        sep = r.right.start
        if a < sep:
            if self.isUsedNode(r.left, a, min(b, sep)):
                return True
        if b > sep:
            if self.isUsedNode(r.right, max(a, sep), b):
                return True
        return False

    def book(self, start: int, end: int) -> bool:
        assert start < end
        if self.isUsedNode(self.root, start, end):
            return False

        self.addNode(self.root, start, end)
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
