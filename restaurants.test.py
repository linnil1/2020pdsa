import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


Restaurants = imp.load_source("Restaurants", 'restaurants.sol.py').Restaurants


def quesion(n, price_lim, distance_lim, query_lim, max_out, small_price=False):
    # init
    np.random.seed()
    id = np.arange(2 * n)
    np.random.shuffle(id)
    id = id[:n]
    rate = np.random.choice(range(1, 6), size=n)
    price = np.random.choice(price_lim, size=n)
    dist = np.random.choice(distance_lim, size=n)
    restaurants = np.stack([id, rate, price, dist]).T
    # print(restaurants)
    ops = [{
        'func': 'init',
        'args': [restaurants],
        'answer': None,
    }]
    sol = Restaurants(restaurants)

    # number to open
    if small_price:
        price = np.random.choice(price_lim, size=(2, query_lim))
        price[1] = price[0] + price_lim // 100
    else:
        price = np.random.choice(price_lim, size=(2, query_lim))
        price = np.stack([price.min(axis=0), price.max(axis=0)])
        # expect 0.1 * N per filter output
        price[1] = price[0] + (price[1] - price[0]) // 2

    rate = np.random.choice(range(1, 6), size=query_lim)
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


# cases = json.load(open("restaurants.json"))
cases = []

cases.append({
    'case': 1,
    'score': 20,
    'data': [
        # 0
        [{'func': 'init',
          'args': [[
              # id, rate, price, distance
              [20, 1, 20, 12],
              [15, 3, 20, 11],
              [19, 5, 20, 12],
              [18, 5, 23, 11]]],
          'answer': None,
         },
         {'func': 'filter', 'args': [0, 18, 5], 'answer': []},
         {'func': 'filter', 'args': [0, 20, 5], 'answer': [19]},
         {'func': 'filter', 'args': [0, 20, 3], 'answer': [15, 19]},
         {'func': 'filter', 'args': [0, 22, 3], 'answer': [15, 19]},
         {'func': 'filter', 'args': [0, 25, 3], 'answer': [18, 15, 19]},
         {'func': 'filter', 'args': [0, 25, 1], 'answer': [18, 15, 20, 19]},
         {'func': 'filter', 'args': [0, 25, 2], 'answer': [18, 15, 19]},
         {'func': 'filter', 'args': [22, 25, 2], 'answer': [18]},
         {'func': 'filter', 'args': [20, 20, 2], 'answer': [15, 19]},
        ],
    ]
})

# 1000 ms * 2
cases.append({
    'case': 2,
    'score': 20,
    'data': [
        # restaurants_len, price, distance, query, max_out
        quesion(100000, 10000, 10000, 1000, 100000 * 10, small_price=True),
        quesion(100000 - 1, 10000, 10000, 1000, 100000 * 10, small_price=True),
    ]
})

# 1000ms
cases.append({
    'case': 3,
    'score': 20,
    'data': [
        # N, restaurants_len, price, distance, query, max_out
        *generateQuestion(10, 1000, 100, 1000, 1000, 1000 * 99),
    ]
})

# 2000ms
cases.append({
    'case': 4,
    'score': 20,
    'data': [
        # N, restaurants_len, price, distance, query, max_out
        quesion(9000, 100,     1000000, 1000, 9000 * 99),
        quesion(9000, 1000000, 1000000, 1000, 9000 * 99),
    ]
})

# 2000ms
cases.append({
    'case': 5,
    'score': 20,
    'data': [
        # N, restaurants_len, price, distance, query, max_out
        quesion(110000, 100000, 1000000, 1000, 110000 * 9),
    ]
})

# 8000 interval -> 1000ms
# 10000 interval -> 1200ms
# 130000 interval -> 2800ms

json.dump(cases, open("restaurants.json", "w"), cls=MyEncoder)
# pprint(cases)
