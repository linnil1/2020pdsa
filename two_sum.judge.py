from Judger import Judger
import imp
Solution = imp.load_source("two_sum", 'two_sum.sol.py').Solution


class Tester(Judger): 
    def __init__(self):
        super().__init__("two_sum.json", debug=True)

    def run(self, sample):
        return Solution().twoSum(sample['nums'], sample['target'])

    def compare(self, out, sample):
        print(out)
        if type(out) is not list:
            return False
        if len(out) != 2:
            return False
        if type(out[0]) is not int or type(out[1]) is not int:
            return False
        return sample['answer'] == out


Tester().judge()
