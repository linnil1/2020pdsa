from typing import List
import math


class Airport:
    def relative(self, a, b):
        return a[0] - b[0], a[1] - b[1]

    def cross(self, va, vb):
        return va[0] * vb[1] - vb[0] * va[1]

    def airport(self, houses: List[List[int]]) -> float:
        """
        Find the best place to build airport and
        calculate the average distance from all the house to airport

        Parameters:
            houses(list[list[int]]): List of houses.
                Each house contains [x,y] coordination.

        Returns:
            distance(float)
        """
        debug = True
        if debug:
            print("# house:", houses)
            max_xy = max(max(i) for i in houses) + 1
            m = [['.'] * max_xy for _ in range(max_xy)]
            for p in houses:
                m[p[1]][p[0]] = '*'
            for i in range(max_xy - 1, -1, -1):
                print(' '.join(m[i]))

        houses = houses
        if len(houses) < 3:
            return 0.

        houses = sorted(houses)
        center = [sum(i[0] for i in houses) / len(houses),
                  sum(i[1] for i in houses) / len(houses)]

        # not start from 3 because maybe in same line
        convex = houses[:2]
        for p in houses[2:]:
            while len(convex) >= 2 and \
                    self.cross(self.relative(convex[-1], convex[-2]),
                               self.relative(         p, convex[-1])) <= 0:
                    convex.pop()
            convex.append(p)

        down_index = len(convex)
        convex.append(houses[-2])
        for p in reversed(houses[:-2]):
            while len(convex) > down_index and \
                    self.cross(self.relative(convex[-1], convex[-2]),
                               self.relative(         p, convex[-1])) <= 0:
                    convex.pop()
            convex.append(p)

        # print(center)
        if debug:
            print("# Convex:", convex[:-1])
        min_dis = math.inf
        for i in range(1, len(convex)):
            vc = self.relative(center, convex[i - 1])
            vb = self.relative(convex[i], convex[i - 1])
            min_dis = min(min_dis, math.fabs(self.cross(vc, vb)) / math.hypot(*vb))

        return min_dis


if __name__ == "__main__":
    print(Airport().airport([[0,0],[1,0]]))
    print(Airport().airport([[0,0],[1,0],[0,1]]))
    # print(Airport().airport([[0,0],[1,0],[2,0]]))
    print(Airport().airport([[0,0],[2,0],[0,2],[1,1],[2,2]]))
    # print(Airport().airport([[9,9],[8,9],[7,9],[11,12],[15,15],[15,10],[15,11]]))
    # print(Airport().airport([[9,9],[8,9],[7,9],[11,13],[15,15],[15,10],[15,11]]))
    print(Airport().airport([[1,1],[2,2],[0,2],[2,0],[2,4],[3,3],[4,2],[4,1],[4,0]]))
    """
    # house: [[0, 0], [1, 0]]
    ..
    **
    0.0
    # house: [[0, 0], [1, 0], [0, 1]]
    *.
    **
    # Convex: [[0, 0], [1, 0], [0, 1]]
    0.2357022603955159
    # house: [[0, 0], [2, 0], [0, 2], [1, 1], [2, 2]]
    *.*
    .*.
    *.*
    # Convex: [[0, 0], [2, 0], [2, 2], [0, 2]]
    1.0
    # house: [[1, 1], [2, 2], [0, 2], [2, 0], [2, 4], [3, 3], [4, 2], [4, 1], [4, 0]]
    ..*..
    ...*.
    *.*.*
    .*..*
    ..*.*
    # Convex: [[0, 2], [2, 0], [4, 0], [4, 2], [2, 4]]
    1.3356461422412562
    """
