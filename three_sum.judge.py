from Judger import Judger
import imp


class Tester(Judger): 
    def __init__(self):
        super().__init__("three_sum.json", debug=True)

    def run(self, sample):
        Solution = imp.load_source("three_sum", 'three_sum.sol.py').Solution
        return Solution().threeSum(sample['nums'])

    def compare(self, out, sample):
        ans = sample['answer']
        if type(out) is not list:
            return False
        if len(out) != len(ans):
            return False
        for i in range(len(ans)):
            if type(out[i]) is not list:
                return False
            if out[i] != ans[i]:
                return False
        return True


Tester().judge()

