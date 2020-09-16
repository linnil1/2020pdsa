from Judger import Judger
import imp


class Tester(Judger): 
    def __init__(self):
        super().__init__("four_sum.json", debug=True)

    def run(self, sample):
        Solution = imp.load_source("four_sum", 'four_sum.sol.py').Solution
        return Solution().fourSum(sample['nums'], sample['target'])

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
#sample={'nums':[-1,0,1,2,3,4],'target':2}
#print(Tester().run(sample))
