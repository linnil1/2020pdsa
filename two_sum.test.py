from typing import List
from collections import defaultdict
import sys
import json
from pprint import pprint

import numpy as np
from tqdm import tqdm


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        ind_dict = {}
        ans = []
        for i, num in enumerate(nums):
            if target - num in ind_dict:
                ans.append([ind_dict[target - num], i])
                if len(ans) > 1:
                    return ans
            ind_dict[num] = i
        return ans


def generateQuestion(N, valueMs, samples=10):
    """
    Generate the question with only one answer
    """
    cases = []
    for _ in tqdm(range(samples)):
        while True:
            # nums = np.random.randint(*valueMs, size=N)
            nums = np.random.choice(np.arange(*valueMs), size=N, replace=False)
            for _ in range(1000):
                ind = np.random.choice(np.arange(n//10, n), size=2, replace=False)
                if len(Solution().twoSum(nums, nums[ind].sum())) == 1:
                    break
            ans = Solution().twoSum(nums, nums[ind].sum())
            if len(ans) == 1:
                if ind[0] > ind[1]:
                    ind = [ind[1], ind[0]]
                if not (ind[0] == ans[0][0] and ind[1] == ans[0][1]):
                    print(ind, ans)
                cases.append({
                    'nums': nums,
                    'target': nums[ind].sum(),
                    'answer': ind,
                })
                break

    pprint(cases)
    return cases


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
# cases = json.load(open("two-sum.json"))

# case1:
cases.append({
    'case': 1,
    'score': 20,
    'data': [{
        'nums': [0, 1],
        'target': 1,
        'answer': [0, 1],
        },{
        'nums': [2, 1],
        'target': 3,
        'answer': [0, 1],
        },{
        'nums': [-1, 1],
        'target': 0,
        'answer': [0, 1],
        },{
        'nums': [2,7,11,15],
        'target': 9,
        'answer': [0, 1],
        },{
        'nums': [3,2,4],
        'target': 6,
        'answer': [1, 2],
        },{
        'nums': [3,4],
        'target': 7,
        'answer': [0, 1],
        },{
        'nums': [2,7,4,15],
        'target': 19,
        'answer': [2, 3],
        }]
})

cases.append({
    'case': 2,
    'score': 20,
    'data': [
        *generateQuestion(10, (-100, 100)),
        *generateQuestion(10, (-10, 10)),
    ]
})

cases.append({
    'case': 3,
    'score': 20,
    'data': generateQuestion(1000, (-100000, 100000))
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion(10000, (-1000000, 1000000))
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion(100000, (-100000000, 100000000))
})

json.dump(cases, open("two_sum.json", "w"), cls=MyEncoder)
