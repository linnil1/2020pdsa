import sys
import json
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import imp


BoardGame = imp.load_source("BoardGame", 'boardgame.sol.py').BoardGame
debug = False
cpu = 32


def quesion(n, m):
    # init
    ops = [{
        'func': 'init',
        'args': [n, n],
        'answer': None,
    }]
    s = BoardGame(n, n)
    cover = 0

    if debug:
        tmpboard = [['.'] * n for _ in range(n)]


    stone = []
    for optype in tqdm(np.random.choice(2, p=[0.5, 0.5], size=m)):
        if optype == 0:
            # put stone in 10x10 near loc
            loc = np.random.choice(n, size=2)
            dif = np.random.choice(11 ** 2, size=18, replace=False)
            dif = np.array([dif // 11, dif % 11]) - 5
            put_stones = []
            for d in range(dif.shape[1]):
                d = loc + dif[:, d]
                if np.all(d >= 0) and np.all(d < n) and (d:= tuple(d)) not in stone:
                    stone.append(d)
                    put_stones.append(d)

            # put on board
            if not put_stones:
                if debug:
                    print("None")
                continue
            cover += len(put_stones)
            chess = np.random.choice(['O', 'X'])
            x, y = list(zip(*put_stones))
            ops.append({
                'func': 'putStone',
                'args': [x, y, chess],
                'answer': s.putStone(x, y, chess)
            })

            # tmp
            # print(put_stones)
            if debug:
                print(put_stones)
                for v in put_stones:
                    tmpboard[v[0]][v[1]] = chess
                print(s)

        elif optype == 1 and len(stone):
            # choose one stone on the board
            a = np.random.choice(len(stone))
            i, j = stone[a]
            ops.append({
                'func': 'surrounded',
                'args': [i, j],
                'answer': s.surrounded(i, j)
            })

    print(cover / n ** 2)
    return ops


def generateQuestion(N, n, m):
    all_ops = []
    with ProcessPoolExecutor(max_workers=cpu) as executor:
        ops = [executor.submit(quesion, n, m) for _ in range(N)]
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


# cases = json.load(open("boardgame.json"))
cases = []
cases.append({
    'case': 1,
    'score': 20,
    'data': [
        # 0
        # .x.
        # x.x
        # .x.
        [{'answer': None,  'func': 'init',       'args': [3, 3]},
         {'answer': None,  'func': 'putStone',   'args': [*zip((0, 1), (1, 0), (1, 2), (2,1)), 'X']},                                   
         {'answer': False, 'func': 'surrounded', 'args': [0, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip((1, 1)), 'O']},
         {'answer': True,  'func': 'surrounded', 'args': [1, 1]}],

        # 1
        # .x.
        # xOx
        # .x.
        [{'answer': None,  'func': 'init',       'args': [3, 3]},
         {'answer': None,  'func': 'putStone',   'args': [*zip([1, 1]), 'O']},
         {'answer': False, 'func': 'surrounded', 'args': [1, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip((0, 1), (1, 0), (1, 2)), 'X']},                                   
         {'answer': False, 'func': 'surrounded', 'args': [0, 1]},
         {'answer': False, 'func': 'surrounded', 'args': [1, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip([2, 1]), 'X']},
         {'answer': False, 'func': 'surrounded', 'args': [0, 1]},
         {'answer': True,  'func': 'surrounded', 'args': [1, 1]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 1]}],

        # 2
        # o
        [{'answer': None,  'func': 'init',       'args': [1, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip([0, 0]), 'O']},
         {'answer': False, 'func': 'surrounded', 'args': [0, 0]}],

        # 3
        # x
        [{'answer': None,  'func': 'init',       'args': [1, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip([0, 0]), 'X']},
         {'answer': False, 'func': 'surrounded', 'args': [0, 0]}],
    ]
})

def case2sample1(n):
    d = []
    for i in range(1, n):
        d.extend([
             {'answer': None,  'func': 'putStone',   'args': [*zip((0, i), (2, i)), 'O']},                                   
             {'answer': None,  'func': 'putStone',   'args': [*zip((1, i), (3, i)), 'X']},                                   
             {'answer': False, 'func': 'surrounded', 'args': [1, 1]},
             {'answer': False, 'func': 'surrounded', 'args': [2, 1]},
             {'answer': False, 'func': 'surrounded', 'args': [1, i]},
             {'answer': False, 'func': 'surrounded', 'args': [2, i]}])
    return d

def case2sample2(n):
    d = [{'answer': None,  'func': 'init',       'args': [4, n]}]
    for i in range(n):
        d.append({'answer': None,  'func': 'putStone',   'args': [*zip((0, i), (2, i)), 'O']})                                  
        d.append({'answer': None,  'func': 'putStone',   'args': [*zip((3, i), (1, i)), 'X']})                                  
        if not i:
            continue
        for x,y in zip(np.random.choice(4, size=4), np.random.choice(i, size=4)):
            d.append({'answer': False, 'func': 'surrounded', 'args': [x, y]})
    return d

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        # 0
        # .ooo x 100
        # oxxx
        # xooo
        # .xxx
        [{'answer': None,  'func': 'init',       'args': [4, 101]},
         *case2sample1(100),
         {'answer': None,  'func': 'putStone',   'args': [*zip((1, 100)), 'O']},                                   
         {'answer': None,  'func': 'putStone',   'args': [*zip((2, 100)), 'X']},                                   
         {'answer': False, 'func': 'surrounded', 'args': [1, 100]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 100]},
         {'answer': False, 'func': 'surrounded', 'args': [1, 99]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 99]},
         {'answer': False, 'func': 'surrounded', 'args': [1, 1]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip((1, 0)), 'O']},                                   
         {'answer': None,  'func': 'putStone',   'args': [*zip((2, 0)), 'X']},                                   
         {'answer': False, 'func': 'surrounded', 'args': [1, 100]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 100]},
         {'answer': True,  'func': 'surrounded', 'args': [1, 99]},
         {'answer': True,  'func': 'surrounded', 'args': [2, 99]},
         {'answer': True,  'func': 'surrounded', 'args': [1, 1]},
         {'answer': True,  'func': 'surrounded', 'args': [2, 1]}],

        # 1
        # .ooo  x 1000
        # oxxx
        # xooo
        # .xxx
        [{'answer': None,  'func': 'init',       'args': [4, 1001]},
         *case2sample1(1000),
         {'answer': None,  'func': 'putStone',   'args': [*zip((1, 1000)), 'O']},                                   
         {'answer': None,  'func': 'putStone',   'args': [*zip((2, 1000)), 'X']},                                   
         {'answer': False, 'func': 'surrounded', 'args': [1, 1000]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 1000]},
         {'answer': False, 'func': 'surrounded', 'args': [1, 999]},
         *[{'answer': False,  'func': 'surrounded', 'args': [2, 999]} for i in range(3000)],
         {'answer': False, 'func': 'surrounded', 'args': [1, 1]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 1]},
         {'answer': None,  'func': 'putStone',   'args': [*zip((1, 0)), 'O']},                                   
         {'answer': None,  'func': 'putStone',   'args': [*zip((2, 0)), 'X']},                                   
         {'answer': False, 'func': 'surrounded', 'args': [1, 1000]},
         {'answer': False, 'func': 'surrounded', 'args': [2, 1000]},
         {'answer': True,  'func': 'surrounded', 'args': [1, 999]},
         *[{'answer': True,  'func': 'surrounded', 'args': [2, 999]} for i in range(3000)],
         {'answer': True,  'func': 'surrounded', 'args': [1, 1]},
         {'answer': True,  'func': 'surrounded', 'args': [2, 1]}],

        # 2
        # oxox x 100
        # xoxo
        # oxox
        # xoxo
        case2sample2(100),
        case2sample2(1000),
    ]
})

cases.append({
    'case': 3,
    'score': 20,
    'data': [
        *generateQuestion(5, 100, 600),
        *generateQuestion(5, 101, 800),
        *generateQuestion(5, 101, 1000),
    ]
})

cases.append({
    'case': 4,
    'score': 20,
    'data': [
        *generateQuestion(2, 1000, 2000),
        *generateQuestion(3, 1001, 3000),
        *generateQuestion(3, 1001, 4000),
    ]
})

cases.append({
    'case': 5,
    'score': 20,
    'data': [
        *generateQuestion(3, 10000, 2000),
        *generateQuestion(2, 10001, 3000),
        *generateQuestion(2, 10001, 4000),
    ]
})

# m
# 450  -> 20ms
# 1800 -> 60ms
# 3200 -> 80ms
# 4000 -> 100ms

json.dump(cases, open("boardgame.json", "w"), cls=MyEncoder)
# pprint(cases)
