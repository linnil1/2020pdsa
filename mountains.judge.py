from Judger import Judger
import sys
import numbers


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("mountains.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Mountains = imp.load_source("Mountains", 'mountains.sol.py').Mountains
        out = Mountains().mountains(sample['mountains'])
        return out

    def compare(self, out, sample):
        if type(out) is not int:
            self.debugPrint('>', sample)
            self.debugPrint('<', out)
            return False
        answer = sample['answer']
        # print(answer)
        if answer != out:
            self.debugPrint('>', sample)
            self.debugPrint('<', out)
        return answer == out


Tester(debug=True).judge()
