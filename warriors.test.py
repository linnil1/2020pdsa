import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Warriors = imp.load_source("Warriors", 'warriors.sol.py').Warriors


def quesion(n):
    # init
    np.random.seed()

    st = np.random.choice(1000, size=n)
    rg = np.random.choice(n, size=n) // 2
    arg = np.stack([st, rg])
    ops = {
        'strength': st,
        'attack_range': rg,
        'answer': Warriors().warriors(st, rg)
    }
    return ops


def generateQuestion(N, n):
    all_ops = []
    with ProcessPoolExecutor(max_workers=20) as executor:
        ops = [executor.submit(quesion, n)
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


# cases = json.load(open("warriors.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
        # 0
        {'strength': [11, 13, 11, 7, 15],
         'attack_range': [ 1,  8,  1, 7,  2],
         'answer': [0, 0, 0, 3, 2, 3, 3, 3, 2, 4]},

        # 1
        {'strength': [11],
         'attack_range': [1],
         'answer': [0, 0]},

        # 2
        {'strength': [11, 15],
         'attack_range': [1, 1],
         'answer': [0, 0, 0, 1]},

        # 3
        {'strength': [11, 15],
         'attack_range': [1, 1],
         'answer': [0, 0, 0, 1]},

        # 4
        {'strength': [15, 11],
         'attack_range': [1, 1],
         'answer': [0, 1, 1, 1]},
    ],
})

for i, arg in enumerate(cases[-1]['data']):
    cases[-1]['data'][i]['answer'] = Warriors().warriors(arg['strength'], arg['attack_range'])

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        # 0
        # increasing
        {'strength':   np.arange(100000),
         'attack_range': np.ones(100000) * 1000000},

        # 1
        # decreasing
        {'strength':   np.flip(np.arange(100000)),
         'attack_range': np.ones(100000) * 1000000},

        # 2
        # increasing + decreasing
        {'strength':   np.hstack([np.arange(100000), np.flip(np.arange(100000))]),
         'attack_range': np.ones(200000) * 4000000},

        # 3
        # decreasing + increasing
        {'strength':   np.hstack([np.flip(np.arange(100000)), np.arange(100000)]),
         'attack_range': np.ones(200000) * 4000000},

        # 4
        # increasing + no attack
        {'strength':   np.arange(100000),
         'attack_range': np.zeros(100000)},

        # 5
        {'strength': [0],
         'attack_range': [1],
         'answer': [0, 0]},

        # 6
        {'strength': [0],
         'attack_range': [0],
         'answer': [0, 0]},

        # 7
        {'strength': [0, 0],
         'attack_range': [0, 0],
         'answer': [0, 0, 1, 1]},

        # 8
        {'strength': [0, 1],
         'attack_range': [0, 0],
         'answer': [0, 0, 1, 1]},
    ],
})

for i, arg in enumerate(cases[-1]['data']):
    cases[-1]['data'][i]['answer'] = Warriors().warriors(arg['strength'], arg['attack_range'])

# 30 * 30 -> 1000ms
cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion(30, 10000),
})

# 2400ms
cases.append({
    'case': 4,
    'score': 20,
    'data': [
        quesion(100000),
        quesion(200000),
        quesion(300000),
        quesion(400000),
    ]
})

# 2400ms
cases.append({
    'case': 5,
    'score': 20,
    'data': [
        quesion(1000000),
    ]
})

# 10000 -> 30ms
# 100000 -> 300ms
# 200000 -> 450ms
# 300000 -> 750ms
# 400000 -> 1000ms
# 500000 -> 1200ms
# 800000 -> 2000ms
# 1000000 -> 2400ms

json.dump(cases, open("warriors.json", "w"), cls=MyEncoder)
# pprint(cases)
