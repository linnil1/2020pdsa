from typing import List
from collections import defaultdict
import sys
import pickle
import json

import numpy as np
from tqdm import tqdm
from pprint import pprint
import imp
import time

Solution = imp.load_source("four_sum", 'four_sum.sol.py').Solution


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
 

def generateQuestion(N, value, samples=10):
    cases = []
    for _ in tqdm(range(samples)):
        s = np.random.randint(N)
        nums = [*np.random.choice(value,       size=s,   replace=False),
                *(-1-np.random.choice(value-1, size=N-s, replace=False))]
        nums = np.array(nums)
        np.random.shuffle(nums)
        ind = np.random.choice(np.arange(N // 10, N), size=4, replace=False)
        target = nums[ind].sum()
        ans = Solution().fourSum(nums, target)
        cases.append({
            'nums': nums.tolist(),
            'target': target,
            'answer': ans
        })
    # pprint(cases)
    return cases


def generateNumSolution(N, valueMs, limit=0,samples=10):
    cases = []
    for _ in tqdm(range(samples)):
        while True:
            nums = np.random.randint(*valueMs, size=N)
            target = np.random.randint(*valueMs)
            ans = Solution().fourSum(nums, target)
            if len(ans) == limit:
                cases.append({
                    'nums': nums.tolist(),
                    'target': target,
                    'answer': ans
                })
                break
    pprint(cases)
    return cases


cases = []
# cases = json.load(open("4sum.json"))
cases.append({
    'case': 1,
    'score': 20,
    'data': [{
        'nums': [1, 0, -1, -2, 2],
        'target': 0,
        'answer': [[-2, -1, 1, 2]],
                   
     }, {
        'nums': [1, -1, 0, -2, 2],
        'target': 100,
        'answer': [],
     }, {
        'nums': [0, 4, 3, 2],
        'target': 1000000,
        'answer': [],
     }, {
        'nums': [-1, -2, -3, -4],
        'target': 0,
        'answer': [],
     }, {
        'nums': [-1, 0, 3, -2],
        'target': 0,
        'answer': [[-2, -1, 0, 3]],
    }]
})

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        *generateQuestion(10, 10),
        *generateQuestion(20, 1000)
    ]
})

cases.append({
    'case': 3,
    'score': 20,
    'data': [{
        'nums': list(range(-100000, -99990)) + list(range(0, 10))  + list(range(  99990, 100000)),
        'target': 87,
        },{
        'nums': list(range(-100000, -99990)) + list(range(10, 20)) + list(range(  99990, 100000)),
        'target': 87,
        },{
        'nums': list(range(-100000, -99990)) + list(range(20, 30)) + list(range(  99990, 100000)),
        'target': 87,
        },{
        'nums': list(range(-100000, -99990)) + list(range(-5, 5))  + list(range(  99990, 100000)),
        'target': 0,
        },{
        'nums': list(range(-100000, -99990)) + list(range(0, 10))  + list(range(  99990, 100000)),
        'target': 0,
    }]
})
for i, d in enumerate(cases[-1]['data']):
    cases[-1]['data'][i]['answer'] = Solution().fourSum(d['nums'], d['target'])
    
cases.append({
    'case': 4,
    'score': 20,
    'data': [
        *generateQuestion(20, 100000000, samples=2),
        *generateQuestion(40, 100000000, samples=2),
        *generateQuestion(60, 100000000, samples=2),
        *generateQuestion(80, 100000000, samples=2),
        *generateQuestion(100, 100000000, samples=2),
    ]
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion(1000, 100000000, samples=1)
})

json.dump(cases, open("four_sum.json", "w"), cls=MyEncoder)
