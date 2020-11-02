from Judger import Judger
import sys
import numbers


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("airport.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Airport = imp.load_source("Airport", 'airport.sol.py').Airport
        out = Airport().airport(sample['houses'])
        return out

    def compare(self, out, sample):
        if not isinstance(out, numbers.Number):
            return False
        if abs(out - sample['answer']) > 1e-4:
            print('<', out)
            print('>', sample['answer'])
            return False
        return True


Tester(debug=True).judge()
# Tester(debug=True).judge()
