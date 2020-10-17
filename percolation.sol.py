class DisjointSet():
    def __init__(self, N :int):
        """ Init N group """
        self.groupid = list(range(N))
        self.group_size = [1] * N
        self.group_num = N
        self.is_open = [False] * N
        self.has_top = [False] * N
        self.has_bottom = [False] * N
        self.is_percolates = False

    def union(self, a :int, b :int):
        """ Merge a and b into one group """
        pa = self.find(a)
        pb = self.find(b)

        if pa != pb:
            # weighted
            if self.group_size[pa] < self.group_size[pb]:
                pa, pb = pb, pa
            self.groupid[pb] = pa
            self.group_size[pa] += self.group_size[pb]
            self.has_top[pa] = self.has_top[pa] or self.has_top[pb]
            self.has_bottom[pa] = self.has_bottom[pa] or self.has_bottom[pb]
            self.group_num -= 1
        if self.has_top[pa] and self.has_bottom[pa]:
            self.is_percolates = True

    def getTop(self, a :int) -> int:
        return self.has_top[self.find(a)]

    def find(self, a :int) -> int:
        """ Find the group id of a """
        """
        while a != self.groupid[a]:
            a = self.groupid[a]
        return a
        """
        if a != self.groupid[a]:
            self.groupid[a] = self.find(self.groupid[a])
        return self.groupid[a]

    def isConnected(self, a :int, b :int) -> bool:
        """ Check a and b is in the same group """
        return self.find(a) == self.find(b)

    def groupSize(self, a :int) -> int:
        """ The size of group """
        return self.group_size[self.find(a)]

    def count(self):
        """ The number of groups in this set """
        return self.group_num


class Percolation():
    def __init__(self, N :int):
        """ Create N-by-N grid, with all sites blocked """
        # 0 -> top
        self.set = DisjointSet(N ** 2)
        self.N = N
        for i in range(N):
            self.set.has_top[self.mapID(0, i)] = True
            self.set.has_bottom[self.mapID(N - 1, i)] = True

    def mapID(self, i, j):
        return i * self.N + j

    def open(self, i :int, j :int):
        """ Open site (row i, column j) if it is not open already """
        # it self
        id = self.mapID(i, j)
        if self.set.is_open[id]:
            raise ValueError
        self.set.is_open[id] = True

        # connect to surround
        for ii, jj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            iii, jjj = i + ii, j + jj
            ij = self.mapID(iii, jjj)
            self.set.union(id, id)
            if (iii >= 0 and iii < self.N and
                jjj >= 0 and jjj < self.N and
                self.set.is_open[ij]):
                self.set.union(id, ij)

    def isOpen(self, i :int, j :int) -> bool:
        """ Is site (row i, column j) open? """
        return self.set.is_open[self.mapID(i, j)]

    def isFull(self, i :int, j :int) -> bool:
        """ Is site (row i, column j) full? """
        id = self.mapID(i, j)
        if not self.set.is_open[id]:
            raise ValueError
        return self.set.getTop(id)

    def percolates(self) -> bool:
        """ Does the system percolate? """
        return self.set.is_percolates

    def __str__(self):
        return "\n".join([
            "".join([str(self.set.is_open[self.mapID(i, j)])[0] for j in range(self.N)])
            for i in range(self.N)])



if __name__ == "__main__":
    s = Percolation(3)
    s.open(1,1)
    # print(s)
    # print(s.set.groupid)
    print(s.isFull(1, 1))
    print(s.percolates())
    s.open(0,1)
    s.open(2,0)
    # print(s)
    # print(s.set.groupid)
    print(s.isFull(1, 1))
    print(s.isFull(0, 1))
    print(s.isFull(2, 0))
    print(s.percolates())
    s.open(1,2)
    s.open(2,2)
    # print(s)
    # print(s.set.groupid)
    print(s.isFull(1, 1))
    print(s.isFull(0, 1))
    print(s.isFull(2, 0))
    print(s.percolates())
