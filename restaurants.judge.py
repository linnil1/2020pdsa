from Judger import Judger
import sys


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("restaurants.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Restaurants = imp.load_source("Restaurants", 'restaurants.sol.py').Restaurants
        s = Restaurants(*sample[0]['args'])
        out = []
        for sam in sample[1:]:
            o = getattr(s, sam['func'])(*sam['args'])
            if sam['answer'] is not None:
                out.append(o)
        return out

    def compare(self, out, sample):
        for i in range(len(out)):
            if type(out[i]) is not list:
                return False
            if out[i] != sample[1 + i]['answer']:
                # print('<', out)
                # print('>', sample[1 + i]['answer'])
                return False
        return True


Tester(debug=True).judge()
# Tester(debug=True).judge()
