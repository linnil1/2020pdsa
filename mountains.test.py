import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Mountains = imp.load_source("Mountains", 'mountains.sol.py').Mountains


def quesion(n, m, value=1000):
    # init
    np.random.seed()

    h = np.random.choice(value, size=(n, m))

    ops = {
        'mountains': h,
        'answer': Mountains().mountains(h)
    }

    return ops


def generateQuestion(args):
    all_ops = []
    with ProcessPoolExecutor(max_workers=20) as executor:
        ops = [executor.submit(quesion, *arg)
               for arg in args]
        for op in as_completed(ops):
            all_ops.append(op.result())
    return all_ops


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


# cases = json.load(open("mountains.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
    {
        'mountains': [[ 0, 1, 2, 3, 4], [24,23,22,21, 5], [12,13,14,15,16], [11,17,18,19,20], [10, 9, 8, 7, 6]],
        'answer': 42
    },
    {
        'mountains': [[3, 4, 5], [9, 3, 5], [7, 4, 3]],
        'answer': 6
    },
    {
        'mountains': [[0, 4, 5], [0, 0, 0], [7, 4, 0]],
        'answer': 0
    },
    {
        'mountains': [[0, 4, 5], [1, 1, 1], [7, 4, 1]],
        'answer': 2
    },
    {
        'mountains': [[1, 4, 5], [1, 1, 1], [7, 4, 0]],
        'answer': 1
    },
]})


def c2q0():
    N = 100
    grid = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            grid[i][j] = i + j

    return {
        'mountains': grid,
        'answer': (N - 1) * 4
    }


def c2q1():
    N = 100
    grid = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            grid[i][j] = min(i + j, 2 * N - 2 - i - j)

    return {
        'mountains': grid,
        'answer': (N - 1) * 3
    }


def c2q2():
    N = 101
    grid = [[0] * N for i in range(N)]
    for i in range(N):
        if i % 4 == 1:
            for j in range(N-1):
                grid[i][j] = 99
        if i % 4 == 3:
            for j in range(1, N):
                grid[i][j] = 99

    return {
        'mountains': grid,
        'answer': 0
    }

def c2q3():
    N = 101
    grid = [[0] * N for i in range(N)]
    q = 0
    for i in range(N):
        if i % 4 == 1:
            for j in range(N-1):
                grid[i][j] = 9999
            grid[i][N-1] = q
            q += 1
        elif i % 4 == 3:
            for j in range(1, N):
                grid[i][j] = 9999
            grid[i][0] = q
            q += 1
        else:
            for j in range(0, N):
                grid[i][j] = q
                q += 1

    return {
        'mountains': grid,
        'answer': Mountains().mountains(grid)
    }


def c2q4():
    q = c2q3()
    q['mountains'] = np.array(q['mountains']).T
    return q

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        c2q0(),
        c2q1(),
        c2q2(),
        c2q3(),
        c2q4(),
        quesion(1, 1000),
        quesion(1000, 1),
    ]
})

cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion([
        *[(30, 30, 1000)] * 20,
    ])
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion([
        *[(100, 100, 1000)] * 8,
        *[(300, 300, 1000)] * 2,
    ])
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion([
        (500, 500, 1000),
    ])
})


json.dump(cases, open("mountains.json", "w"), cls=MyEncoder)
pprint(cases)
"""
10*1000    67.16ms
100*100    74.68ms
100*1000   800.71ms
10*10000   680.77ms
1000*1000  8893.76ms
"""
