import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Airport = imp.load_source("Airport", 'airport.sol.py').Airport


def quesion(n, limit=1000):
    # init
    np.random.seed()

    pos = np.random.choice(1000, size=(n, 2))
    pos = np.unique(pos, axis=0)
    np.random.shuffle(pos)
    ops = {
        'houses': pos,
        'answer': Airport().airport(list([list(i) for i in pos]))
    }
    return ops


def generateQuestion(N, n, limit):
    all_ops = []
    with ProcessPoolExecutor(max_workers=20) as executor:
        ops = [executor.submit(quesion, n, limit)
               for _ in range(N)]
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


# cases = json.load(open("airport.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
        {'houses': [[0,0],[1,0]]},
        {'houses': [[0,0],[1,0],[0,1]]},
        {'houses': [[0,0],[2,0],[0,2],[1,1],[2,2]]},
        {'houses': [[0,0],[1,0],[2,0]]},
        {'houses': [[9,9],[8,9],[7,9],[11,12],[15,15],[15,10],[15,11]]},

        {'houses': [[9,9],[8,9],[7,9],[11,13],[15,15],[15,10],[15,11]]},
        {'houses': [[1,1],[2,2],[0,2],[2,0],[2,4],[3,3],[4,2],[4,1],[4,0]]},
        {'houses': [[3,3],[3,2],[3,1],[1,3],[2,3],[3,4],[3,5],[4,3],[5,3]]},

        {'houses': [[3,3],[3,2],[3,1],[1,3],[2,3]]},
        {'houses': [[3,3],[3,4],[3,5],[4,3],[5,3]]},
        {'houses': [[3,3],[1,3],[2,3],[3,4],[3,5]]},
        {'houses': [[3,3],[4,3],[5,3],[3,2],[3,1]]},
    ],
})

for i in range(len(cases[-1]['data'])):
    cases[-1]['data'][i]['answer'] = Airport().airport(cases[-1]['data'][i]['houses'])


def sample0(n=50000, r=100000):
    # circle
    th = np.linspace(0, np.pi * 2, n)
    pos = np.array([np.cos(th) * r + r, np.sin(th) * r + r]).T
    pos = pos.astype(np.int)
    
    pos = np.unique(pos, axis=0)
    np.random.shuffle(pos)
    print(pos.shape)
    return {'houses': pos}

def sample1(n=10000, r=10000):
    # square
    pos = []
    an = np.arange(n + 1)
    one = np.ones(n + 1, dtype=np.int)
    pos.append(np.array([an * i , r * one]).T)
    pos.append(np.array([r * one, an * i ], dtype=np.int).T)
    pos.append(np.array([an * i , 0 * one]).T)
    pos.append(np.array([0 * one, an * i ], dtype=np.int).T)
    pos.append(np.array([an * i,  an * i ], dtype=np.int).T)
    pos.append(np.array([an * i, r - an * i], dtype=np.int).T)
    pos = np.concatenate(pos)
    pos = np.unique(pos, axis=0)
    np.random.shuffle(pos)
    print(pos.shape)
    return {'houses': pos}

def sample2(n=230):
    # grids
    pos = []
    cx, cy = np.meshgrid(np.arange(n + 1), np.arange(n + 1))
    pos = np.array([cx.flatten(), cy.flatten()]).T
    pos = np.unique(pos, axis=0)
    np.random.shuffle(pos)
    print(pos.shape)
    return {'houses': pos}

def sample3(n=10000):
    # 5 lines
    pos = []
    an = np.arange(n + 1)
    s = set()
    for _ in range(6):
        while True:
            dx, dy = np.random.choice(np.arange(-12, 13), size=2)
            if dy != 0 and dx != 0 and dy / dx not in s:
                s.add(dy / dx)
                break
        pos.append(np.array([dx * an, dy * an], dtype=np.int).T)
    pos = np.concatenate(pos)
    pos += pos.min(axis=0)
    pos = np.unique(pos, axis=0)
    np.random.shuffle(pos)
    print(pos.shape)
    return {'houses': pos}


cases.append({
    'case': 2,
    'score': 20,
    'data': [
        sample0(),
        sample1(),
        sample2(),
        sample3(),
    ]
})

for i in range(len(cases[-1]['data'])):
    cases[-1]['data'][i]['answer'] = Airport().airport(list([list(i) for i in cases[-1]['data'][i]['houses']]))

cases.append({
    'case': 3,
    'score': 20,
    'data': [
        *generateQuestion(4, 10, 10),
        *generateQuestion(4, 30, 10),
        *generateQuestion(4, 50, 10),
        *generateQuestion(4, 80, 10),
        *generateQuestion(4, 100, 10),
    ]
})

cases.append({
    'case': 4,
    'score': 20,
    'data': [
        *generateQuestion(4, 10, 1000),
        *generateQuestion(4, 100, 1000),
        *generateQuestion(4, 1000, 1000),
        *generateQuestion(4, 10000, 1000),
    ]
})

cases.append({
    'case': 5,
    'score': 20,
    'data': [
        *generateQuestion(3, 100000, 100000),
    ]
})

# 10000: 70ms
# 50000: 400ms
# 100000: 700ms

json.dump(cases, open("airport.json", "w"), cls=MyEncoder)
# pprint(cases)
