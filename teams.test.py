import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Teams = imp.load_source("Teams", 'teams.sol.py').Teams


def quesion(n, limit=1000, falselimit=None):
    # init
    np.random.seed()

    if falselimit is None:
        tf = np.random.choice([True, False])
        falselimit = limit // 100
    elif falselimit > 0:
        tf = False
    else:
        tf = True

    id = np.arange(n)
    np.random.shuffle(id)
    s = np.random.choice(np.arange(1, n-1))
    id1 = id[s:]
    id2 = id[:s]
    graph = []

    cid1 = np.random.choice(id1, size=limit)
    cid2 = np.random.choice(id2, size=limit)
    graph =  np.stack([cid1, cid2]).T

    if not tf:
        cid1 = np.random.choice(id1, size=(falselimit, 2))
        cid2 = np.random.choice(id2, size=(falselimit, 2))
        graph = np.vstack([graph, cid1, cid2])

    graph = np.unique(graph, axis=0)
    np.random.shuffle(graph)
    # print(graph)

    if not tf:
        tf = Teams().teams(n, graph)

    ops = {
        'idols': n,
        'teetee': graph,
        'answer': bool(tf),
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


# cases = json.load(open("teams.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
    {
        'idols': 4,
        'teetee': [[0,1],[0,3],[2,1],[3,2]],
        'answer': True,
    },
    {
        'idols': 4,
        'teetee': [[0,1],[0,3],[0,2],[2,1],[3,2]],
        'answer': False,
    },
    {
        'idols': 2,
        'teetee': [[0,1]],
        'answer': True,
    },
    {
        'idols': 3,
        'teetee': [[0,1], [1,2]],
        'answer': True,
    },
    {
        'idols': 3,
        'teetee': [[0,1], [1,2], [0,2]],
        'answer': False,
    },
    {
        'idols': 4,
        'teetee': [[0,1],[2,3]],
        'answer': True,
    },
    {
        'idols': 5,
        'teetee': [[0,1],[2,3],[3,4]],
        'answer': True,
    },
    {
        'idols': 5,
        'teetee': [[0,1],[2,1], [2,3], [3,4]],
        'answer': True,
    },
    {
        'idols': 5,
        'teetee': [[0,1],[2,1], [2,3], [3,4], [0,4]],
        'answer': False,
    },
]})


def c2q1():
    # 1 vs all
    graph = []
    n = 10000
    for i in range(1, n):
        graph.append([0, i])

    return {
        'idols': n,
        'teetee': graph,
        'answer': True,
    }

def c2q2():
    # n vs n full degree
    graph = []
    n = 100
    for i in range(n):
        for j in range(n):
            graph.append([i, n + j])

    return {
        'idols': n,
        'teetee': graph,
        'answer': True,
    }

def c2q3():
    # n vs n full degree flase
    graph = []
    n = 100
    for i in range(n):
        for j in range(n):
            graph.append([i, n + j])
    graph.append([0, 1])

    return {
        'idols': 2 * n,
        'teetee': graph,
        'answer': False,
    }

def c2q4():
    # linear
    graph = []
    n = 10000
    graph.append([0, n - 1])
    for i in range(1, n):
        graph.append([i - 1, i])

    return {
        'idols': n,
        'teetee': graph,
        'answer': True,
    }

def c2q5():
    # linear false
    graph = []
    n = 10001
    graph.append([0, n - 1])
    for i in range(1, n):
        graph.append([i - 1, i])

    return {
        'idols': n,
        'teetee': graph,
        'answer': False,
    }

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        c2q1(),
        c2q2(),
        c2q3(),
        c2q4(),
        c2q5(),
    ]
})


# for v in cases[-1]['data']:
#     v['answer'] = Teams().teams(list([list(i) for i in v['points']]), v['cluster_num'])

cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion([
        (10,  10, 0),
        (10,  50, 0),
        (10,  100, 0),
        (10,  100, 10),
        (100,  100, 0),
        (100,  100, 10),
        (1000,  10, 0),
        (1000,  100, 0),
        (1000,  100, 10),
        (1000,  1000, 0),
        (1000,  1000, 10),
    ])
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion([
        (10000,  1000, 0),
        (10000,  1000, 10),
        (10000,  1000, 100),
        (10000,  5000, 0),
        (10000, 10000, 0),
        (10000, 10000, 10),
    ])
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion([
        (100000, 400000, 0),
        (100000, 400000, 10),
    ])
})


json.dump(cases, open("teams.json", "w"), cls=MyEncoder)
# pprint(cases)
"""
197.89ms -> 100000
110.33ms -> 100000
3008.93ms -> 1000000
35038.66ms -> 10000000
"""
