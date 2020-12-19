import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Cluster = imp.load_source("Cluster", 'cluster.sol.py').Cluster


def quesion(n, limit=1000):
    # init
    np.random.seed()

    while True:
        pos = np.random.choice(limit, size=(n, 2))
        num = np.random.choice(range(2, 6))
        pos = np.unique(pos, axis=0)
        np.random.shuffle(pos)
        num = min(len(pos), num)
        try:
            ops = {
                'points': pos,
                'cluster_num': num,
                'answer': Cluster().cluster(list([list(i) for i in pos]), num)
            }
            break
        except ValueError:
            continue

    print(n, "OK")
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


# cases = json.load(open("cluster.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
        {'points': [[3,0], [0,0], [1,0], [0,1]],
         'cluster_num': 2},
        {'points': [[0,0], [3,0], [1,0], [0,1]],
         'cluster_num': 2},
        {'points': [[0,0], [1,0], [3,0], [0,1]],
         'cluster_num': 2},
        {'points': [[0,0], [1,0], [0,1], [3,0]],
         'cluster_num': 2},
        {'points': [[0,3], [3,3], [4,7], [9,0], [9,4]],
         'cluster_num': 3},
        {'points': [[0,1], [0,2], [3,1], [3,2]],
         'cluster_num': 2},
    ],
})

for v in cases[-1]['data']:
    v['answer'] = Cluster().cluster(list([list(i) for i in v['points']]), v['cluster_num'])

def sample2case1():
    p = [[0, 0]]
    n = 200
    for i in range(1, n):
        p.append([p[-1][0] + i, 0])
    return {'points': p,
            'cluster_num': 2}

def sample2case2():
    n = 11
    p = []
    for i in range(n):
        for j in range(n):
            p.append([i + 0,   j + 0])
            p.append([i + 100, j + 100])
            p.append([i + 0,   j + 100])
            p.append([i + 100, j + 0])
    return {'points': p,
            'cluster_num': 4}


def sample2case3():
    n = 20
    p = []
    for i in range(n):
        for j in range(n):
            p.append([i, j])
    p.append([100, 100])
    return {'points': p,
            'cluster_num': 2}

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        # sample2case1(),  # this is ambiuous
        sample2case2(),
        sample2case3(),
    ],
})

for v in cases[-1]['data']:
    v['answer'] = Cluster().cluster(list([list(i) for i in v['points']]), v['cluster_num'])

cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion([
        (10, 100),
        (20, 100),
        (30, 100),
        (40, 100),
        (50, 100),
        (60, 100),
        (70, 100),
        (80, 100),
        (90, 100),
        (100, 100),
    ])
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion([
        (100, 1000),
        (200, 1000),
        (300, 1000),
        (400, 1000),
    ])
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion([(700, 10000)])
})

json.dump(cases, open("cluster.json", "w"), cls=MyEncoder)
# pprint(cases)
"""
100      28.77ms
200      106.70ms
400      545.51ms
700      2008.22ms
800      2708.22ms
1000      3107.55ms
"""
