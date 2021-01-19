import sys 
from typing import List
sys.setrecursionlimit(100001)


class Eulercycle:
    def eulercycle(self, num_node:int, edges:List[int]) -> List[int]:
        # build edge list for nodes
        node_edges = [[] for i in range(num_node)]
        for i in range(len(edges)):
            node_edges[edges[i][0]].append(i)
            node_edges[edges[i][1]].append(i)

        # dfs
        used = [False] * len(edges)
        path = []
        def dfs(f):
            for i in node_edges[f]:
                if used[i]:
                    continue
                used[i] = True
                if edges[i][0] == f:
                    to = edges[i][1]
                else:
                    to = edges[i][0]
                dfs(to)
            path.append(f)

        dfs(0)
        print(path)
        return path


def toEdge(a):
    return [[min(a[i-1:i+1]), max(a[i-1:i+1])] for i in range(1, len(a))]


if __name__ == "__main__":
    edges = [[0,1],[1,2],[0,2]]
    path = Eulercycle().eulercycle(3, edges)
    # [0, 2, 1, 4, 3, 1, 0]
    print(len(path) == len(edges) + 1 and
          sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))

    edges = [[0,1],[1,2],[0,2], [1,3],[1,4], [3,4]]
    path = Eulercycle().eulercycle(5, edges)
    # [0, 2, 1, 4, 3, 1, 0]
    print(len(path) == len(edges) + 1 and
          sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))

    edges = [[0,1],[1,2],[0,2], [1,4],[1,3], [3,4]]
    path = Eulercycle().eulercycle(5, edges)
    print(len(path) == len(edges) + 1 and
          sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))

    edges = [[0,1],[1,2],[0,2], [0,4],[0,3], [3,4]]
    path = Eulercycle().eulercycle(5, edges)
    # [0, 3, 4, 0, 2, 1, 0]
    print(len(path) == len(edges) + 1 and
          sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))

    edges = [[0,1],[1,2],[0,2], [0,3],[0,4], [3,4]]
    path = Eulercycle().eulercycle(5, edges)
    print(len(path) == len(edges) + 1 and
          sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))

    edges = [[0,1],[1,2],[0,2], [0,0]]
    path = Eulercycle().eulercycle(3, edges)
    # [0, 0, 2, 1, 0]
    print(len(path) == len(edges) + 1 and
          sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))
