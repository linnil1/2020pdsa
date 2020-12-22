import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Railway = imp.load_source("Railway", 'railway.sol.py').Railway


def quesion(n, limit, valueLimit=1000):
    # init
    np.random.seed()

    ids = np.random.choice(n, size=(limit, 2))
    dist = np.random.choice(valueLimit, size=(limit, 1))
    graph =  np.hstack([ids, dist])

    # remove self-link
    # graph = graph[graph[:, 0] != graph[:, 1]]
    # remove duplicated-link
    # graph = np.unique(graph, axis=0)
    # np.random.shuffle(graph)
    dist = Railway().railway(n, graph)

    ops = {
        'landmarks': n,
        'distance': graph,
        'answer': dist
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


# cases = json.load(open("railway.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
    {
        'landmarks': 4,
        'distance': [[0,1,2], [0,2,4], [1,3,5], [2,1,1]],
        'answer': 8
    },
    {
        'landmarks': 4,
        'distance': [[0,1,0], [0,2,4], [0,3,4], [1,2,1], [1,3,4], [2,3,2]],
        'answer': 3
    },
    {
        'landmarks': 3,
        'distance': [[0,1,0], [0,2,0]],
        'answer': 0
    },
    {
        'landmarks': 3,
        'distance': [[0,1,1], [0,2,2], [1,2,3]],
        'answer': 3
    },
    {
        'landmarks': 2,
        'distance': [[0,1,0]],
        'answer': 0
    },
    {
        'landmarks': 2,
        'distance': [[0,1,3]],
        'answer': 3
    },
    {
        'landmarks': 1,
        'distance': [[0,0,5]],
        'answer': 0
    },
    {
        'landmarks': 2,
        'distance': [[0,1,9], [0,1,1], [0,1,20]],
        'answer': 1
    },
]})


def c2q1():
    # linear all is 1
    graph = []
    n = 10001
    for i in range(1, n):
        graph.append([i - 1, i, 1])

    return {
        'landmarks': n,
        'distance': graph,
        'answer': n - 1,
    }


def c2q2():
    # linear duplicated
    graph = []
    n = 10001
    for i in range(1, n):
        graph.append([i - 1, i, 1])
        graph.append([i - 1, i, 100])

    return {
        'landmarks': n,
        'distance': graph,
        'answer': n - 1,
    }


def c2q3():
    # complete
    graph = []
    n = 100
    for i in range(n):
        for j in range(n):
            graph.append([i, j, 1])

    return {
        'landmarks': n,
        'distance': graph,
        'answer': n - 1,
    }

def c2q4():
    # linaer increaing
    graph = []
    n = 10000
    for i in range(1, n):
        graph.append([i - 1, i, i])

    return {
        'landmarks': n,
        'distance': graph,
        'answer': (n) * (n - 1) // 2,
    }


def c2q5():
    # linaer decreaing
    graph = []
    n = 10000
    for i in range(n - 1, 0, -1):
        graph.append([i - 1, i, i])

    return {
        'landmarks': n,
        'distance': graph,
        'answer': (n) * (n - 1) // 2,
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
#     v['answer'] = Railway().railway(list([list(i) for i in v['points']]), v['cluster_num'])

cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion([
        # (1000, 10000, 100),
        *[(10, 50)] * 4,
        *[(10, 60)] * 4,
        *[(10, 70)] * 4,
        *[(10, 80)] * 4,
        *[(10, 90)] * 4,
    ])
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion([
        *[(100,  1000, 1000)] * 6,
        *[(100,  10000, 1000)]  * 6,
        *[(1000, 10000, 10000)] * 2,
        *[(1000, 100000, 10000)] * 2,
        *[(1000, 100000, 1000)] * 2,
        *[(1000, 100000, 100)] * 2,
    ])
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion([
        (10000, 1000000, 10000),
    ])
})


json.dump(cases, open("railway.json", "w"), cls=MyEncoder)
pprint(cases)
"""
23.53ms    Edge = 10000
208.50ms   Edge = 100000
2295.70ms  Edge = 1000000

"""
