from collections import defaultdict
from typing import List
from queue import Queue


class Teams:
    def teams(self, idols: int, teetee: List[List[int]]) -> bool:
        # build the graph
        self.nodes = defaultdict(list)
        for i,j in teetee:
            self.nodes[i].append(j)
            self.nodes[j].append(i)

        # bfs start
        self.color = {}
        for i in self.nodes:
            if i not in self.color:
                if not self.bfs(i):
                    return False
        return True

    def bfs(self, i):
        now = True
        self.color[i] = now
        q = Queue()
        q.put(i)
        while not q.empty():
            node = q.get()
            node_color = self.color[node]
            for i in self.nodes[node]:
                if i not in self.color:
                    self.color[i] = not node_color
                    q.put(i)
                elif self.color[i] == node_color:
                    return False
        return True


if __name__ == "__main__":
    print(Teams().teams(4, [[0,1],[0,3],[2,1],[3,2]]))
    print(Teams().teams(4, [[0,1],[0,3],[0,2],[2,1],[3,2]]))
