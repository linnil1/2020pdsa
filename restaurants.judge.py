from Judger import Judger
import sys
import functools
import imp


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("restaurants.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        Restaurant  = imp.load_source("Restaurant" , "restaurants.sol.py").Restaurant
        Restaurants = imp.load_source("Restaurants", "restaurants.sol.py").Restaurants
        rests = [Restaurant(*i) for i in sample[0]['args'][0]]
        self.resetTime()
        if sample[0]['func'] == "init":
            sol = Restaurants(rests)
        out = []
        for sam in sample[1:]:
            if sam['func'] == "filter":
                out.append(getattr(sol, sam['func'])(*sam['args']))
            elif sam['func'] == "sortN":
                out.append([i.getID() for i in sorted(rests)])
            elif sam['func'] == "sortD":
                out.append([i.getID() for i in sorted(rests, key=functools.cmp_to_key(Restaurant.comparator1))])
        return out

    def compare(self, out, sample):
        for i in range(len(out)):
            if type(out[i]) is not list:
                return False
            if out[i] != sample[i + 1]['answer']:
                print(sample[i + 1], out[i])
                return False
        return True


Tester(debug=True).judge()
# Tester(debug=True).judge()
