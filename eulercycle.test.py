import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Eulercycle = imp.load_source("Eulercycle", 'eulercycle.sol.py').Eulercycle

def toEdge(a):
    return [[min(a[i-1:i+1]), max(a[i-1:i+1])] for i in range(1, len(a))]


def quesion(n, limit=1000):
    # init
    np.random.seed()

    path = list(np.random.randint(limit, size=n))
    num = set(path)
    for i in range(limit):
        if i not in num:
            path.append(i)
    path.append(path[0])

    # dege
    edge = toEdge(path)
    np.random.shuffle(edge)

    ops = {
        'node': limit,
        'edge': edge
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


# cases = json.load(open("eulercycle.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
    {
        'node': 3,
        'edge': [[0,1],[1,2],[0,2]]
    },
    {
        'node': 5,
        'edge': [[0,1],[1,2],[0,2], [1,3],[1,4], [3,4]]
    },
    {
        'node': 5,
        'edge': [[0,1],[1,2],[0,2], [1,4],[1,3], [3,4]]
    },
    {
        'node': 5,
        'edge': [[0,1],[1,2],[0,2], [1,4],[1,3], [3,4]]
    },
    {
        'node': 5,
        'edge': [[0,1],[1,2],[0,2], [0,4],[0,3], [3,4]]
    },
    {
        'node': 5,
        'edge': [[0,1],[1,2],[0,2], [0,3],[0,4], [3,4]]
    },
    ]
})


cases.append({
    'case': 2,
    'score': 20,
    'data': generateQuestion([
        *[(i * 10, 10) for i in range(1, 51)],
    ])
})

cases.append({
    'case': 3,
    'score': 30,
    'data': generateQuestion([
        *[(i * 100, 100) for i in range(1, 51)],
    ])
})

cases.append({
    'case': 4,
    'score': 30,
    'data': generateQuestion([
        *[(5000, 1000)] * 50,
    ])
})


json.dump(cases, open("eulercycle.json", "w"), cls=MyEncoder)
# pprint(cases)
