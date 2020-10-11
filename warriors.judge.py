from Judger import Judger
import sys


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("warriors.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Warriors = imp.load_source("Warriors", 'warriors.sol.py').Warriors
        out = Warriors().warriors(sample['strength'], sample['attack_range'])
        return out

    def compare(self, out, sample):
        if type(out) is not list:
            return False
        if out != sample['answer']:
            # print('<', out)
            # print('>', sample[1 + i]['answer'])
            return False
        return True


Tester(debug=True).judge()
# Tester(debug=True).judge()
