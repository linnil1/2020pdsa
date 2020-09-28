import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Percolation = imp.load_source("Percolation", 'percolation.sol.py').Percolation


def quesion(n):
    # init
    ops = [{
        'func': 'init',
        'args': [n],
        'answer': None,
    }]
    s = Percolation(n)

    # number to open
    loc = np.arange(n ** 2)
    np.random.shuffle(loc)
    now = 0
    for optype in tqdm(np.random.choice(3, p=[0.6, 0.2, 0.2], size=int(n ** 2 * 0.8 / 0.2))):
        if optype == 0 and now:
            a = np.random.choice(loc[:now])
            i, j = a // n, a % n
            ops.append({
                'func': 'isFull',
                'args': [i, j],
                'answer': s.isFull(i, j)
            })
        elif optype == 1:
            ops.append({
                'func': 'precolates',
                'args': [],
                'answer': s.precolates()
            })
        elif optype == 2:
            if now >= len(loc):
                return ops
            a = loc[now]
            now += 1
            i, j = a // n, a % n
            ops.append({
                'func': 'open',
                'args': [i, j],
                'answer': s.open(i, j)
            })

    return ops


def generateQuestion(N, n):
    all_ops = []
    with ProcessPoolExecutor(max_workers=30) as executor:
        ops = [executor.submit(quesion, n) for _ in range(N)]
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


# cases = json.load(open("percolation.json"))
cases = []
cases.append({
    'case': 1,
    'score': 20,
    'data': [
        # 0
        [{'func': 'init',       'args': [1],    'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'open',       'args': [0, 0], 'answer': None},
         {'func': 'isFull',     'args': [0, 0], 'answer': True},
         {'func': 'precolates', 'args': [],     'answer': True}],

        # 1
        [{'func': 'init',       'args': [1],    'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'open',       'args': [0, 0], 'answer': None},
         {'func': 'precolates', 'args': [],     'answer': True},
         {'func': 'isFull',     'args': [0, 0], 'answer': True}],

        # 2
        [{'func': 'init',       'args': [3],    'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'open',       'args': [1, 1], 'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'isFull',     'args': [1, 1], 'answer': False},
         {'func': 'open',       'args': [0, 1], 'answer': None},
         {'func': 'isFull',     'args': [1, 1], 'answer': True},
         {'func': 'isFull',     'args': [0, 1], 'answer': True},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'open',       'args': [2, 0], 'answer': None},
         {'func': 'isFull',     'args': [2, 0], 'answer': False},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'isFull',     'args': [1, 1], 'answer': True},
         {'func': 'open',       'args': [2, 1], 'answer': None},
         {'func': 'isFull',     'args': [2, 1], 'answer': True},
         {'func': 'precolates', 'args': [],     'answer': True},
         {'func': 'isFull',     'args': [2, 0], 'answer': True}]
    ]
})

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        # 0
        # xox
        # xoo
        # oxo
        [{'func': 'init',       'args': [3],    'answer': None},
         {'func': 'open',       'args': [1, 1], 'answer': None},
         {'func': 'open',       'args': [0, 1], 'answer': None},
         {'func': 'open',       'args': [2, 0], 'answer': None},
         {'func': 'open',       'args': [2, 2], 'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'open',       'args': [1, 2], 'answer': None},
         {'func': 'isFull',     'args': [2, 0], 'answer': False},
         {'func': 'isFull',     'args': [2, 2], 'answer': True},
         {'func': 'precolates', 'args': [],     'answer': True},
         {'func': 'isFull',     'args': [2, 0], 'answer': False}],

        # 1
        # ooo
        # ooo
        # ooo
        [{'func': 'init',       'args': [3],    'answer': None},
         {'func': 'open',       'args': [0, 0], 'answer': None},
         {'func': 'open',       'args': [0, 1], 'answer': None},
         {'func': 'open',       'args': [0, 2], 'answer': None},
         {'func': 'open',       'args': [1, 0], 'answer': None},
         {'func': 'open',       'args': [1, 1], 'answer': None},
         {'func': 'open',       'args': [1, 2], 'answer': None},
         {'func': 'open',       'args': [2, 0], 'answer': None},
         {'func': 'open',       'args': [2, 1], 'answer': None},
         {'func': 'open',       'args': [2, 2], 'answer': None},
         {'func': 'precolates', 'args': [],     'answer': True},
         {'func': 'isFull',     'args': [1, 1], 'answer': True},
         {'func': 'isFull',     'args': [2, 2], 'answer': True},
         {'func': 'isFull',     'args': [0, 0], 'answer': True}],

        # 2
        # ooooo
        # oxxxo
        # oxoxo
        # oxxxo
        # ooooo
        [{'func': 'init',       'args': [5],    'answer': None},
         {'func': 'open',       'args': [0, 0], 'answer': None},
         {'func': 'open',       'args': [0, 1], 'answer': None},
         {'func': 'open',       'args': [0, 2], 'answer': None},
         {'func': 'open',       'args': [0, 3], 'answer': None},
         {'func': 'open',       'args': [0, 4], 'answer': None},
         {'func': 'open',       'args': [4, 0], 'answer': None},
         {'func': 'open',       'args': [4, 1], 'answer': None},
         {'func': 'open',       'args': [4, 2], 'answer': None},
         {'func': 'open',       'args': [4, 3], 'answer': None},
         {'func': 'open',       'args': [4, 4], 'answer': None},
         {'func': 'open',       'args': [1, 0], 'answer': None},
         {'func': 'open',       'args': [2, 0], 'answer': None},
         {'func': 'open',       'args': [3, 0], 'answer': None},
         {'func': 'open',       'args': [1, 4], 'answer': None},
         {'func': 'open',       'args': [2, 4], 'answer': None},
         {'func': 'open',       'args': [3, 4], 'answer': None},
         {'func': 'open',       'args': [2, 2], 'answer': None},
         {'func': 'isFull',     'args': [2, 2], 'answer': False},
         {'func': 'precolates', 'args': [],     'answer': True},
         {'func': 'isFull',     'args': [4, 2], 'answer': True},
         {'func': 'isFull',     'args': [2, 2], 'answer': False},
         {'func': 'open',       'args': [2, 1], 'answer': None},
         {'func': 'isFull',     'args': [2, 2], 'answer': True},
         {'func': 'precolates', 'args': [],     'answer': True}],

        # 3
        # xx
        # oo
        [{'func': 'init',       'args': [2],    'answer': None},
         {'func': 'open',       'args': [1, 0], 'answer': None},
         {'func': 'open',       'args': [1, 1], 'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'isFull',     'args': [1, 0], 'answer': False},
         {'func': 'isFull',     'args': [1, 1], 'answer': False},
         {'func': 'precolates', 'args': [],     'answer': False}],

        # 4
        # oxo
        # xox
        # oxo
        [{'func': 'init',       'args': [3],    'answer': None},
         {'func': 'open',       'args': [1, 1], 'answer': None},
         {'func': 'open',       'args': [0, 0], 'answer': None},
         {'func': 'open',       'args': [2, 2], 'answer': None},
         {'func': 'open',       'args': [2, 0], 'answer': None},
         {'func': 'open',       'args': [0, 2], 'answer': None},
         {'func': 'precolates', 'args': [],     'answer': False},
         {'func': 'isFull',     'args': [1, 1], 'answer': False},
         {'func': 'isFull',     'args': [2, 2], 'answer': False},
         {'func': 'isFull',     'args': [2, 0], 'answer': False},
         {'func': 'isFull',     'args': [0, 2], 'answer': True},
         {'func': 'precolates', 'args': [],     'answer': False}],

        # 5
        # xxxxxo
        # xoooxo
        # xoxoxo
        # xoxoxo
        # xoxoxo
        # xoxooo
        # xoxxxx
    ]
})

"""
cases.append({
    'case': 3,
    'score': 20,
    'data': [
        *generateQuestion(20, 50),
    ]
})

cases.append({
    'case': 4,
    'score': 20,
    'data': [
        *generateQuestion(6, 100),
    ]
})

cases.append({
    'case': 5,
    'score': 20,
    'data': [
        *generateQuestion(1, 250),
    ]
})
"""

# 50 -> 40ms
# 100 -> 150ms
# 200 -> 650ms
# 250 -> 1s
# 300 -> 1.4s
# 1000 -> 18s
json.dump(cases, open("percolation.json", "w"), cls=MyEncoder)
pprint(cases)
