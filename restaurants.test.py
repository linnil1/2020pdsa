import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp
import functools


Restaurant = imp.load_source("Restaurant", 'restaurants.sol.py').Restaurant
Restaurants = imp.load_source("Restaurants", 'restaurants.sol.py').Restaurants


def quesion(n, price_lim, distance_lim, query_lim, max_out, small_price=False, small_rate=False):
    # init
    np.random.seed()
    id = np.arange(n * 2)
    np.random.shuffle(id)
    id = id[:n]
    rate = np.random.choice(range(1, 6), size=n)
    if small_rate:
        rate = np.random.choice(range(1, 6), p=[0.6, 0.2, 0.1, 0.05, 0.05], size=n)
    price = np.random.choice(price_lim, size=n)
    dist = np.random.choice(distance_lim, size=n)
    restaurants = np.stack([id, rate, price, dist]).T
    # print(restaurants)
    ops = [{
        'func': 'init',
        'args': [restaurants],
        'answer': None,
    }]
    sol = Restaurants([Restaurant(*i) for i in restaurants])

    # number to open
    if small_price:
        price = np.random.choice(price_lim, size=(2, query_lim))
        price[1] = price[0] + price_lim // 100
    else:
        price = np.random.choice(price_lim, size=(2, query_lim))
        price = np.stack([price.min(axis=0), price.max(axis=0)])
        # expect 0.1 * N per filter output
        price[1] = price[0] + (price[1] - price[0]) // 2

    # generate rate
    rate = np.random.choice(range(1, 6), size=query_lim)
    if small_rate:
        rate = np.random.choice(range(1, 6), p=[0.05, 0.05, 0.1, 0.2, 0.6], size=n)

    all_ans_len = 0
    for p_min, p_max, r in tqdm(zip(price[0], price[1], rate)):
        ans = sol.filter(p_min, p_max, r)
        all_ans_len += len(ans)
        ops.append({
            'func': 'filter',
            'args': [p_min, p_max, r],
            'answer': ans
        })

        if all_ans_len >= max_out:
            break
    print("out_len", all_ans_len)
    return ops


def quesionSort(n, price_lim, distance_lim):
    # init
    np.random.seed()
    id = np.arange(n * 2)
    np.random.shuffle(id)
    id = id[:n]
    rate = np.random.choice(range(1, 6), size=n)
    price = np.random.choice(price_lim, size=n)
    dist = np.random.choice(distance_lim, size=n)
    restaurants = np.stack([id, rate, price, dist]).T
    rests = [Restaurant(*i) for i in restaurants]
    # print(restaurants)
    return [{
        'func': "sort",
        'args': [restaurants],
        'answer': None,
    },{
        'func': "sortN",
        'args': [],
        'answer': [i.id for i in sorted(rests)],
    },{
        'func': "sortD",
        'args': [],
        'answer': [i.id for i in sorted(rests, key=functools.cmp_to_key(Restaurant.comparator1))]
    }]


def generateQuestion(N, n, price, distance, query, max_out):
    all_ops = []
    with ProcessPoolExecutor(max_workers=20) as executor:
        ops = [executor.submit(quesion, n, price, distance, query, max_out)
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


cases = []
cases.append({
    'case': 1,
    'score': 20,
    'data': [
        # 0
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [3, 3, 3, 3]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [0, 5, 4], 'answer': []},
         {'func': 'filter', 'args': [5, 9, 4], 'answer': []},
         {'func': 'filter', 'args': [5, 9, 1], 'answer': []},
         {'func': 'filter', 'args': [0, 2, 1], 'answer': []},
         {'func': 'filter', 'args': [0, 5, 3], 'answer': [3]},
         {'func': 'filter', 'args': [0, 5, 2], 'answer': [3]},
        ],

        # 1
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [0, 5, 20, 10],
              [1, 4, 21, 11],
              [2, 3, 22, 12],
              [3, 2, 23, 13],
              [4, 1, 24, 14]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [0, 18, 5], 'answer': []},
         {'func': 'filter', 'args': [0, 20, 5], 'answer': [0]},
         {'func': 'filter', 'args': [0, 21, 5], 'answer': [0]},
         {'func': 'filter', 'args': [0, 25, 1], 'answer': [0, 1, 2, 3, 4]},
         {'func': 'filter', 'args': [0, 25, 3], 'answer': [0, 1, 2]},
         {'func': 'filter', 'args': [21, 25, 5], 'answer': []},
         {'func': 'filter', 'args': [21, 25, 3], 'answer': [1,2]},
         {'func': 'filter', 'args': [21, 25, 2], 'answer': [1,2,3]},
        ],

        # 2
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [0, 1, 20, 10],
              [1, 2, 21, 11],
              [2, 3, 22, 12],
              [3, 4, 23, 13],
              [4, 5, 24, 14]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [0, 25, 5], 'answer': [4]},
         {'func': 'filter', 'args': [0, 20, 1], 'answer': [0]},
         {'func': 'filter', 'args': [0, 21, 4], 'answer': []},
         {'func': 'filter', 'args': [0, 25, 1], 'answer': [0, 1, 2, 3, 4]},
         {'func': 'filter', 'args': [0, 25, 3], 'answer': [2, 3, 4]},
         {'func': 'filter', 'args': [0, 25, 2], 'answer': [1, 2, 3, 4]},
         {'func': 'filter', 'args': [21, 25, 2], 'answer': [1, 2, 3, 4]},
        ],

        # 3
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [50, 1, 20, 10],
              [41, 2, 21, 11],
              [32, 3, 22, 12],
              [23, 4, 23, 13],
              [14, 5, 24, 14]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [0, 25, 5], 'answer': [14]},
         {'func': 'filter', 'args': [0, 20, 1], 'answer': [50]},
         {'func': 'filter', 'args': [0, 21, 4], 'answer': []},
         {'func': 'filter', 'args': [0, 25, 1], 'answer': [50, 41, 32, 23, 14]},
         {'func': 'filter', 'args': [0, 25, 2], 'answer': [41, 32, 23, 14]},
         {'func': 'filter', 'args': [0, 25, 3], 'answer': [32, 23, 14]},
         {'func': 'filter', 'args': [21, 25, 2], 'answer': [41, 32, 23, 14]},
        ],

        # 4
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [50, 1, 2, 10],
              [41, 2, 2, 12],
              [32, 3, 2, 12],
              [23, 4, 22, 13],
              [14, 5, 22, 14]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [10, 20, 5], 'answer': []},
         {'func': 'filter', 'args': [10, 20, 1], 'answer': []},
         {'func': 'filter', 'args': [0, 20, 1], 'answer': [50, 41, 32]},
         {'func': 'filter', 'args': [0, 20, 1], 'answer': [50, 41, 32]},
        ],

        # 5
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [0, 3, 20, 10],
              [1, 3, 21, 10],
              [3, 4, 22, 13],
              [4, 4, 24, 14]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [10, 25, 3], 'answer': [1, 0, 3, 4]},
         {'func': 'filter', 'args': [10, 25, 4], 'answer': [3, 4]},
         {'func': 'filter', 'args': [10, 20, 5], 'answer': []},
        ],
    ]
})

# 1000 ms * 2
cases.append({
    'case': 2,
    'score': 20,
    'data': [
        # restaurants_len, price, distance, query, max_out
        quesion(100000, 10000, 10000, 1000, 100000 * 9, small_price=True),
        quesion(50000,  10000, 10000, 1000, 50000 * 9, small_rate=True),
    ]
})

# 1000ms
cases.append({
    'case': 3,
    'score': 20,
    'data': [
        # N, restaurants_len, price, distance, query, max_out
        *generateQuestion(10, 1000, 100, 100, 1000, 1000 * 99),
    ]
})


# 2000ms
cases.append({
    'case': 4,
    'score': 20,
    'data': [
        # N, restaurants_len, price, distance, query, max_out
        quesion(9000, 100,   10000, 1000, 9000 * 99),
        quesion(9000, 10000, 10000, 1000, 9000 * 99),
    ]
})

# 2000ms
cases.append({
    'case': 5,
    'score': 10,
    'data': [
        # N, restaurants_len, price, distance, query, max_out
        quesion(100000, 10000, 10000, 1000, 100000 * 9),
    ]
})

# sort
cases.append({
    'case': 6,
    'score': 10,
    'data': [
        quesionSort(10, 10, 10),
        quesionSort(1000, 10, 10),
        quesionSort(100, 100, 100),
        quesionSort(1000, 1000, 1000),
        quesionSort(10000, 10000, 10000),
    ]
})

# 8000 interval -> 1000ms
# 10000 interval -> 1200ms
# 130000 interval -> 2800ms

# cases = [*cases, *json.load(open("restaurants.json"))[2:]]
json.dump(cases, open("restaurants.json", "w"), cls=MyEncoder)
# pprint(cases)
