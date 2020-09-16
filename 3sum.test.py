import json
import numpy as np
from tqdm import tqdm
from pprint import pprint
import imp


Solution = imp.load_source("3sum", '3sum.sol.py').Solution


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


def generateQuestion(N, valueMs, length=-1, samples=10):
    cases = []
    for _ in tqdm(range(samples)):
        while True:
            # nums = np.random.randint(*valueMs, size=N)
            nums = np.random.choice(np.arange(*valueMs), size=N, replace=False)
            ans = Solution().threeSum(nums)
            if (length == -1 and len(ans) > 0) or len(ans) == length:
                cases.append({
                    'nums': nums,
                    'answer': ans
                })
                break
    return cases


cases = []
cases = json.load(open("3sum.json"))
cases.append({
    'case': 1,
    'score': 20,
    'data': [{
        'nums': [-1,0,1,2,-2,-4],
        'answer': [[-2,0,2],[-1,0,1]],
        },{
        'nums': [-1,0,1,2],
        'answer': [[-1,0,1]],
        },{
        'nums': [-1,-3,0,1,2],
        'answer': [[-3,1,2], [-1,0,1]],
        }
    ]
})
        
cases.append({
    'case': 2,
    'score': 20,
    'data': [{
        'nums': [0,1],
        'answer': [],
        },{
        'nums': [0,2,1],
        'answer': [],
        },{
        'nums': [],
        'answer': [],
        },{
        'nums': [0],
        'answer': [],
        },{
        'nums': [0,1,-1],
        'answer': [[-1, 0, 1]],
        }, {
        'nums': list(range(20)),
        'answer': [],
        }, {
        'nums': [10, 0] + list(range(40, 60)) + [-10],
        'answer': [[-10, 0, 10]],
        }, {
        'nums': [-10, -11, -12, -13, -14, -15,
                  10,  11,  12,  13,  14,  15],
        'answer': []
    }]
})

cases.append({
    'case': 3,
    'score': 20,
    'data': [
        *generateQuestion(10, (-10, 10), length=0, samples=5),
        *generateQuestion(10, (-10, 10), length=1, samples=5),
        *generateQuestion(10, (-10, 10), length=2, samples=5),
    ]
})

cases.append({
    'case': 4,
    'score': 20,
    'data': generateQuestion(1000, (-100000, 100000))
})

cases.append({
    'case': 5,
    'score': 20,
    'data': generateQuestion(1000, (-100000000, 100000000))
})

json.dump(cases, open("3sum.json", "w"), cls=MyEncoder)
