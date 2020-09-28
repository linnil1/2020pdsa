import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


DisjointSet = imp.load_source("DisjointSet", 'disjoint.sol.py').DisjointSet


def quesion(n):
    ops = [{
        'func': 'init',
        'args': [n],
        'answer': None,
    }]
    s = DisjointSet(n)

    op_num = np.random.choice(np.arange(n * 2, n * 5 // 2))
    all_n = np.arange(n)
    for optype in tqdm(np.random.choice(4, p=[0.5, 0.2, 0.2, 0.1], size=op_num)):
        if optype == 0:
            a, b = np.random.choice(all_n, size=2, replace=False)
            ops.append({
                'func': 'union',
                'args': [a, b],
                'answer': s.union(a, b)
            })
        elif optype == 1:
            a, b = np.random.choice(all_n, size=2, replace=False)
            ops.append({
                'func': 'isConnected',
                'args': [a, b],
                'answer': s.isConnected(a, b)
            })
        elif optype == 2:
            a = np.random.choice(all_n)
            ops.append({
                'func': 'groupSize',
                'args': [a],
                'answer': s.groupSize(a)
            })
        else:
            ops.append({
                'func': 'count',
                'args': [],
                'answer': s.count()
            })
    return ops


def generateQuestion(N, n):
    all_ops = []
    with ProcessPoolExecutor(max_workers=16) as executor:
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


cases = json.load(open("disjoint.json"))
cases = []
cases.append({
    'case': 1,
    'score': 20,
    'data': [
        [{'func': 'init', 'args': [1], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [0], 'answer': 1}],

        [{'func': 'init', 'args': [3], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3},
         {'func': 'groupSize', 'args': [1], 'answer': 1},
         {'func': 'union', 'args': [1, 2], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 2},
         {'func': 'groupSize', 'args': [1], 'answer': 2},
         {'func': 'groupSize', 'args': [2], 'answer': 2},
         {'func': 'groupSize', 'args': [0], 'answer': 1},
         {'func': 'isConnected', 'args': [0, 1], 'answer': False},
         {'func': 'isConnected', 'args': [2, 1], 'answer': True}],

        [{'func': 'init', 'args': [3], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3},
         {'func': 'groupSize', 'args': [1], 'answer': 1},
         {'func': 'union', 'args': [2, 1], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 2},
         {'func': 'groupSize', 'args': [1], 'answer': 2},
         {'func': 'groupSize', 'args': [2], 'answer': 2},
         {'func': 'groupSize', 'args': [0], 'answer': 1},
         {'func': 'isConnected', 'args': [0, 1], 'answer': False},
         {'func': 'isConnected', 'args': [2, 1], 'answer': True}],

        [{'func': 'init', 'args': [3], 'answer': None},
         {'func': 'union', 'args': [1, 2], 'answer': None},
         {'func': 'union', 'args': [0, 2], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [1], 'answer': 3},
         {'func': 'groupSize', 'args': [2], 'answer': 3},
         {'func': 'count', 'args': [], 'answer': 1}],

        [{'func': 'init', 'args': [3], 'answer': None},
         {'func': 'groupSize', 'args': [1], 'answer': 1},
         {'func': 'union', 'args': [1, 2], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 2},
         {'func': 'groupSize', 'args': [1], 'answer': 2},
         {'func': 'union', 'args': [1, 2], 'answer': None},
         {'func': 'union', 'args': [1, 2], 'answer': None},
         {'func': 'union', 'args': [1, 2], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 2},
         {'func': 'groupSize', 'args': [1], 'answer': 2},
         {'func': 'union', 'args': [0, 2], 'answer': None},
         {'func': 'groupSize', 'args': [1], 'answer': 3},
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'union', 'args': [0, 2], 'answer': None},
         {'func': 'union', 'args': [0, 2], 'answer': None},
         {'func': 'union', 'args': [0, 2], 'answer': None},
         {'func': 'union', 'args': [0, 2], 'answer': None},
         {'func': 'groupSize', 'args': [1], 'answer': 3},
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'count', 'args': [], 'answer': 1}],

        [{'func': 'init', 'args': [100], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 100},
         *([{'func': 'groupSize', 'args': [0], 'answer': 1}] * 100)],

        [{'func': 'init', 'args': [100], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 100},
         *([{'func': 'groupSize', 'args': [0], 'answer': 1}] * 100)],

    ]
})

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        [{'func': 'init', 'args': [3000], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3000},
         *[{'func': 'union', 'args': [i, i+1], 'answer': None} for i in range(3000 - 1)],
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [0], 'answer': 3000},
         {'func': 'groupSize', 'args': [2999], 'answer': 3000},
         {'func': 'groupSize', 'args': [1300], 'answer': 3000},
         {'func': 'isConnected', 'args': [0, 2999], 'answer': True}],

        [{'func': 'init', 'args': [3000], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3000},
         *[{'func': 'union', 'args': [i, i+1], 'answer': None} for i in range(3000 - 1)],
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [0], 'answer': 3000},
         {'func': 'groupSize', 'args': [2999], 'answer': 3000},
         {'func': 'groupSize', 'args': [1300], 'answer': 3000},
         *([{'func': 'isConnected', 'args': [0, 2999], 'answer': True}] * 3000)],

        [{'func': 'init', 'args': [3000], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3000},
         *[{'func': 'union', 'args': [i + 1, i], 'answer': None} for i in range(3000 - 1)],
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [0], 'answer': 3000},
         {'func': 'groupSize', 'args': [2999], 'answer': 3000},
         {'func': 'groupSize', 'args': [1300], 'answer': 3000},
         *([{'func': 'isConnected', 'args': [0, 2999], 'answer': True}] * 3000)],

        [{'func': 'init', 'args': [3000], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3000},
         *[{'func': 'union', 'args': [i, i - 1], 'answer': None} for i in range(2999, 0, -1)],
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [0], 'answer': 3000},
         {'func': 'groupSize', 'args': [2999], 'answer': 3000},
         {'func': 'groupSize', 'args': [1300], 'answer': 3000},
         *([{'func': 'isConnected', 'args': [0, 2999], 'answer': True}] * 3000)],

        [{'func': 'init', 'args': [3000], 'answer': None},
         {'func': 'count', 'args': [], 'answer': 3000},
         *[{'func': 'union', 'args': [i - 1, i], 'answer': None} for i in range(2999, 0, -1)],
         {'func': 'count', 'args': [], 'answer': 1},
         {'func': 'groupSize', 'args': [0], 'answer': 3000},
         {'func': 'groupSize', 'args': [2999], 'answer': 3000},
         {'func': 'groupSize', 'args': [1300], 'answer': 3000},
         *([{'func': 'isConnected', 'args': [0, 2999], 'answer': True}] * 3000)],
    ]
})
cases.append({
    'case': 3,
    'score': 20,
    'data': [
        *generateQuestion(10, 100),
        *generateQuestion(10, 101)
    ]
})

cases.append({
    'case': 4,
    'score': 20,
    'data': [
        *generateQuestion(10, 10000),
        *generateQuestion(10, 10001)
    ]
})

cases.append({
    'case': 5,
    'score': 20,
    'data': [
        *generateQuestion(3, 100000),
    ]
})

json.dump(cases, open("disjoint.json", "w"), cls=MyEncoder)
# pprint(cases)
