from typing import List
import sys
sys.setrecursionlimit(100001)



class DisjointSet:
    def __init__(self, n):
        self.N = n
        self.n = n
        self.id = list(range(n))

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            self.n -= 1
            self.id[a] = b
            return True
        else:
            return False

    def find(self, a):
        if a == self.id[a]:
            return a
        self.id[a] = self.find(self.id[a])
        return self.id[a]


class Railway():
    def __init__(self):
        pass
    
    def railway(self, nodes:int, edges: List[List[int]]) -> int:
        edges = sorted(edges, key=lambda a: a[2])
        # print(edges)
        self.set = DisjointSet(nodes)
        cost = 0
        for a, b, w in edges:
            if self.set.union(a, b):
                cost += w
        if self.set.n != 1:
            raise ValueError("Graph not connect")
        return cost


if __name__ == "__main__":
    print(
    Railway().railway(4,[[0,1,2],
                         [0,2,4], 
                         [1,3,5], 
                         [2,1,1]])
    )
    # Answer: 8 (2 + 5 + 1)
    # (the railway from 0 to 2 cannot be added because 0 and 2 are already connected)

    print(
    Railway().railway(4,[[0,1,0],
                         [0,2,4], 
                         [0,3,4], 
                         [1,2,1], 
                         [1,3,4], 
                         [2,3,2]])
    )
    # Answer: 3(0 + 1 + 2)
