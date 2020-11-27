from typing import List
import heapq
import math


class DisjointSet():
    def __init__(self, N :int):
        """ Init N group """
        self.groupid = list(range(N))
        self.group_size = [1] * N
        self.size = N

    def union(self, a :int, b :int):
        """ Merge a and b into one group """
        pa = self.find(a)
        pb = self.find(b)
        if pa != pb:
            if self.group_size[pa] < self.group_size[pb]:
                pa, pb = pb, pa
            self.groupid[pb] = pa
            self.group_size[pa] += self.group_size[pb]
            self.size -= 1

    def find(self, a :int) -> int:
        """ Find the group id of a """
        if a != self.groupid[a]:
            self.groupid[a] = self.find(self.groupid[a])
        return self.groupid[a]


class Cluster:
    def distance(self, a, b):
        a = self.center[a]
        b = self.center[b]
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def merge(self, a, b):
        new_index = len(self.size)
        self.size.append(self.size[a] + self.size[b])
        p = [0, 0]
        p[0] += self.center[a][0] * self.size[a]
        p[1] += self.center[a][1] * self.size[a]
        p[0] += self.center[b][0] * self.size[b]
        p[1] += self.center[b][1] * self.size[b]
        p[0] /= self.size[new_index]
        p[1] /= self.size[new_index]
        self.center.append(p)
        self.size[a] = self.size[b] = 0
        self.N -= 1
        self.link[a] = new_index
        self.link[b] = new_index
        return new_index

    def listCluster(self):
        for i, s in enumerate(self.size):
            if s:
                yield i

    def find(self, a :int) -> int:
        """ Find the group id of a """
        if a != self.link[a]:
            self.link[a] = self.find(self.link[a])
        return self.link[a]

    def cluster(self, points: List[List[int]], cluster_num: int) -> List[List[float]]:
        """
        Cluster the points to cluster_num clusters.
        """
        # init
        self.center = points
        self.N = len(points)
        self.now_size = 1
        self.size = [1] * self.N
        self.heap = []
        self.link = list(range(self.N * 2))
        self.set = DisjointSet(self.N * 2)

        # add to heap
        for i in range(self.N):
            self.heap.extend((self.distance(i, j), i, j) for j in range(i + 1, self.N))
        heapq.heapify(self.heap)

        # merge and add to heap
        small_old = 1e99
        while self.N > cluster_num:
            small_dis, i, j = heapq.heappop(self.heap)
            discard = False
            if not self.size[i] or not self.size[j]:
                continue

            tmp = [heapq.heappop(self.heap)]
            while tmp[-1][0] - small_dis < 1e-3:
                self.set.union(tmp[-1][1], tmp[-1][2])
                tmp.append(heapq.heappop(self.heap))
            while len(tmp):
                heapq.heappush(self.heap, tmp.pop())

            # merge
            self.set.union(i, j)
            j = self.merge(i, j)
            self.set.union(i, j)

            # add to heap
            for i in self.listCluster():
                if i != j:
                    heapq.heappush(self.heap, (self.distance(i, j), i, j))

        # print("disjoint", self.set.groupid)
        # print("link    ", self.link)
        for i in range(self.N):
            if self.set.find(i) != self.set.find(self.find(i)):
                print(i, self.find(i))
                raise ValueError("Order matter1")
        for i in self.listCluster():
            for j in self.listCluster():
                if i < j and self.set.find(i) == self.set.find(j):
                    print(i, j)
                    raise ValueError("Order matter2")

        return sorted([self.center[i] for i in self.listCluster()])


if __name__ == "__main__":
    print(Cluster().cluster([[0,0], [1,0], [3,0], [0,1]], 2))
    # [[0.3333333333333333, 0.3333333333333333], [3, 0]]

    print(Cluster().cluster([[0,3], [3,3], [4,7], [9,0], [9,4]], 3))
    # [[1.5, 3.0], [4, 7], [9.0, 2.0]]

    print(Cluster().cluster([[0,1], [0,2], [3,1], [3,2]], 2))
    # [[0.0, 1.5], [3.0, 1.5]]
    # print(Cluster().cluster([[0,0], [1,0], [0,1]], 2))
