import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Calendar = imp.load_source("Calendar", 'calendar.sol1.py').Calendar


def quesion(n, limit=1000, cover=100):
    # init
    np.random.seed()

    start = np.random.choice(limit, size=n)
    end = np.random.choice(limit // cover, size=n) + 1
    end += start
    end = np.clip(end, 0, limit)

    ops = [{
        'func': 'init',
        'args': [],
        'answer': None,
    }]
    s = Calendar()

    for i in range(n):
        ops.append({
            'func': "book",
            'args': [start[i], end[i]],
            'answer': s.book(start[i], end[i])
        })

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


# cases = json.load(open("calendar.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
        # 0
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [15, 20],  'answer': True},
        ],
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [1,  3],   'answer': True},
        ],
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [10, 18],  'answer': True},
        ],
        # 3
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [15, 20],  'answer': True},
         {'func': 'book', 'args': [5, 10],   'answer': False},
         {'func': 'book', 'args': [15, 20],  'answer': False},
        ],
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [8, 20],   'answer': False},
        ],
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [6,  8],   'answer': False},
        ],
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [1,  8],   'answer': False},
        ],
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 10],   'answer': True},
         {'func': 'book', 'args': [1, 18],   'answer': False},
        ],
        # 8
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [10, 20],   'answer': True},
         {'func': 'book', 'args': [15, 25],   'answer': False},
         {'func': 'book', 'args': [20, 25],   'answer': True},
         {'func': 'book', 'args': [17, 21],   'answer': False},
         {'func': 'book', 'args': [0, 3],   'answer': True},
         {'func': 'book', 'args': [2, 6],   'answer': False},
         {'func': 'book', 'args': [3, 6],   'answer': True},
        ],
        # 9
        [{'func': 'init', 'args': [],        'answer': None},
         {'func': 'book', 'args': [5, 15],   'answer': True},
         {'func': 'book', 'args': [0, 18],   'answer': False},
         {'func': 'book', 'args': [24, 29],   'answer': True},
         {'func': 'book', 'args': [13, 25],   'answer': False},
         {'func': 'book', 'args': [18, 22],   'answer': True},
         {'func': 'book', 'args': [15, 18],   'answer': True},
        ],
    ],
})

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        [{'func': 'init', 'args': [],         'answer': None},
         *[{'func': 'book', 'args': [i, i+1], 'answer': True} for i in range(10000)],
         {'func': 'book', 'args': [5, 10],    'answer': False},
        ],
        [{'func': 'init', 'args': [],         'answer': None},
         *[{'func': 'book', 'args': [i, i+1], 'answer': True} for i in range(9999, -1, -1)],
         {'func': 'book', 'args': [5, 10],    'answer': False},
        ],
        quesion(10000, 200000, 200000),
        # [{'func': 'init', 'args': [],         'answer': None},
        #  {'func': 'book', 'args': [9999, 10001],  'answer': True},
        #  *[{'func': 'book', 'args': [i, i+10000], 'answer': False} for i in range(10000)],
        #  {'func': 'book', 'args': [0, 10],    'answer': True},
        # ],
    ]
})

# for v in cases[-1]['data']:
#     v['answer'] = Calendar().calendar(list([list(i) for i in v['points']]), v['cluster_num'])

cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion([
        ( 200, 1000),
        ( 400, 1000),
        ( 600, 1000),
        ( 800, 1000),
        (1000, 1000),
    ])
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion([
        ( 2000, 10000),
        ( 4000, 10000),
        ( 6000, 10000),
        ( 8000, 10000),
        (10000, 1000),
        (10000, 10000, 1000),
        (10000, 10000, 10),
        (10000, 10000),
        (10000, 20000),
        (20000, 20000),
    ])
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion([
        (120000, 1000000),
    ])
})


json.dump(cases, open("calendar.json", "w"), cls=MyEncoder)
# pprint(cases)
"""
"""
