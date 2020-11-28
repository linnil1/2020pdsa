from Judger import Judger
import sys
import numbers


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("calendar.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Calendar = imp.load_source("Calendar", 'calendar.sol2.py').Calendar
        sol = Calendar()
        out = [sol.book(*s['args']) for s in sample[1:]]
        return out

    def compare(self, out, sample):
        if out != [s['answer'] for s in sample[1:]]:
            print('<', out)
            print('>', sample)
            return False
        return True


Tester(debug=True).judge()
# Tester(debug=True).judge()
