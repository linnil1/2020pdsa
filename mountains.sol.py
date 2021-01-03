# linnil1
# dijkstra
from typing import List
import heapq
from pprint import pprint


class Mountains:
    def mountains(self, grid: List[List[int]]) -> int:
        N = len(grid)
        M = len(grid[0])
        mm = 10 ** 8
        dist = [mm] * (N * M)
        parent = [0] * (N * M)
        id_s = 0
        id_e = N * M - 1
        verbose = False

        parent[0] = 0
        dist[id_s] = 0
        pq = [(dist[id_s], id_s)]
        while True:
            dis, id = heapq.heappop(pq)
            if id == id_e:
                if verbose:
                    pprint(grid)
                    stack = []
                    i = id_e
                    while i != id_s:
                        stack.append((dist[i], grid[i // M][i % M], (i // M, i % M)))
                        i = parent[i]
                    j = 0, grid[id_s // M][id_s % M], (0, 0)
                    for i in reversed(stack):
                        print(f"From {j[2]}(height={j[1]:2d}) "
                              f"to {i[2]}(height={i[1]:2d}) "
                              f"takes {i[0] - j[0]:2}; total: {i[0]:2}")
                        j = i
                return dist[id]

            x, y = id // M, id % M
            for i,j in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                i, j = i + x, j + y
                if 0 <= i < N and 0 <= j < M:
                    newid = i * M + j

                    if grid[x][y] > grid[i][j]:
                        min_path = (grid[x][y] - grid[i][j])
                    else:
                        min_path = (grid[i][j] - grid[x][y]) * 2
                    min_path += dist[id]

                    if min_path < dist[newid]:
                        dist[newid] = min_path
                        parent[newid] = id
                        heapq.heappush(pq, (min_path, newid))

        
if __name__ == "__main__":
    print(Mountains().mountains(
        [[ 0, 1, 2, 3, 4],
         [24,23,22,21, 5],
         [12,13,14,15,16],
         [11,17,18,19,20],
         [10, 9, 8, 7, 6]]))
    # ans=42
    print(Mountains().mountains(
        [[3, 4, 5],
         [9, 3, 5],
         [7, 4, 3]]))
    # ans=6
