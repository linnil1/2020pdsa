class DisjointSet():
    def __init__(self, N :int):
        """ Init N group """
        self.groupid = list(range(N))
        self.group_size = [1] * N
        self.group_num = N

    def union(self, a :int, b :int):
        """ Merge a and b into one group """
        pa = self.find(a)
        pb = self.find(b)
        if pa != pb:
            if self.group_size[pa] < self.group_size[pb]:
                pa, pb = pb, pa
            self.groupid[pb] = pa
            self.group_size[pa] += self.group_size[pb]
            self.group_num -= 1

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


if __name__ == "__main__":
    s = DisjointSet(3)
    s.union(1, 2)
    print(s.count())
    print(s.isConnected(1, 2))
    print(s.isConnected(0, 2))
    print(s.groupSize(0))
    print(s.groupSize(1))
    print(s.groupSize(2))
