from typing import List
from collections import deque


class DisjointSet():
    def __init__(self, N :int):
        """ Init N group """
        self.groupid = list(range(N))
        self.group_size = [1] * N

        # chess game specific
        self.no_surround_num = [0] * N
        self.chesses = ['.'] * N

    def add(self, chess :str) -> int:
        """ Add one element in the set """
        id = len(self.groupid)
        self.group_size.append(1)
        self.groupid.append(id)

        # chess game specific
        self.chesses.append(chess)
        self.no_surround_num.append(0)
        return id

    def surroundUpdate(self, a: int, num: int):
        """ Update no_surround_num of the group by adding num """
        self.no_surround_num[self.find(a)] += num

    def union(self, a :int, b :int):
        """ Merge a and b into one group """
        pa = self.find(a)
        pb = self.find(b)
        if pa != pb:
            if self.group_size[pa] < self.group_size[pb]:
                pa, pb = pb, pa
            self.groupid[pb] = pa
            self.group_size[pa] += self.group_size[pb]
            self.no_surround_num[pa] += self.no_surround_num[pb]

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


class BoardGame:
    def __init__(self, h :int, w :int):
        """
        Set the width and height of the board

        Parameters:
            h (int): The height of the board
            w (int): The width of the board
        """
        self.set = DisjointSet(0)
        self.map = {}

    def putStone(self, x :List[int], y :List[int], stoneType :str):
        """
        Put the stones on (x[0],y[0]), (x[1], y[1]) ...

        We grantee there are not stones on (x[i],y[i]) in the board.

        Parameters:
            x (int): The height position of the stone, 0 <= x <= h
            y (int): The width position of the stone, 0 <= y <= w
            stoneType (string): The type of the stone, which has only two values {'O', 'X'}
        """
        for i in range(len(x)):
            self.putOneStone(x[i], y[i], stoneType)

    def putOneStone(self, x :int, y :int, stone_type:str):
        """ Put the stone on (x,y) """
        # Update myself
        id = self.set.add(stone_type)
        self.map[(x, y)] = id
        self.set.surroundUpdate(id, 4)

        # find surrounded o and x
        for ii, jj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ij = (x + ii, y + jj)
            if ij in self.map:
                ij = self.map[ij]
                if self.set.chesses[ij] == stone_type:
                    self.set.surroundUpdate(id, -2)
                    self.set.union(id, ij)
                else:  # self.set.chesses[ij] != stone_type:
                    self.set.surroundUpdate(id, -1)
                    self.set.surroundUpdate(ij, -1)

    def surrounded(self, x :int, y :int) -> bool:
        """
        Give if the connected stones can be flipped,

        i.e. Stones are surrounded by another type of stones.

        Parameters:
            x (int): The height position of the stone, 0 <= x <= h
            y (int): The width position of the stone, 0 <= y <= w
        Returns:
            can_flip (bool): Can be flipped of not.
        """
        id = self.set.find(self.map[(x, y)])
        return self.set.no_surround_num[id] == 0

    def getStoneType(self, x :int, y :int) -> str:
        """
        Get the type of the stone on (x,y)

        We grantee that there are stones on (x,y)

        Parameters:
            x (int): The height position of the stone, 0 <= x <= h
            y (int): The width position of the stone, 0 <= y <= w
        Returns:
            stoneType (string): The type of the stones, which has only two value {'O', 'X'}
        """
        id = self.set.find(self.map[(x, y)])
        return self.set.chesses[id]

    def __str__(self):
        board = [['.'] * self.N for _ in range(self.N)]
        for i, j in self.map.items():
            board[i[0]][i[1]] = self.set.chesses[j]
        return "\n".join([(''.join(i)) for i in board]) + "\n"


if __name__ == "__main__":
    g = BoardGame(5, 5)
    """
    .....
    ..x..
    .xox.
    ..x..
    .....
    """
    g.putStone(*zip((1, 2), (2, 1), (2, 3), (3, 2)), 'X')
    g.putStone(*zip((2, 2)), 'O')
    print(g.surrounded(1, 2))
    print(g.surrounded(2, 2))
    g.putStone(*zip((0, 2), (1, 1), (2, 0)), 'O')
    g.putStone(*zip((2, 4), (3, 3), (4, 4)), 'O')
    g.putStone(*zip((3, 1), (1, 3)), 'O')
    print(g.surrounded(2, 2))
    print(g.surrounded(2, 3))
    print(g.surrounded(2, 4))
    # g.flipChess('O')
    # g.flipChess('X')

    print("here")
    g = BoardGame(3, 3)
    g.putStone([1], [1], 'O')
    print(g.surrounded(1, 1))
    g.putStone([0, 1, 1], [1, 0, 2], 'X')
    print(g.surrounded(1, 1))
    g.putStone([2], [1], 'X')
    print(g.surrounded(1, 1))
    print(g.surrounded(2, 1))
