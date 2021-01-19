from Judger import Judger
import sys
import numbers


def toEdge(a):
    return [[min(a[i-1:i+1]), max(a[i-1:i+1])] for i in range(1, len(a))]


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("eulercycle.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Eulercycle = imp.load_source("Eulercycle", 'eulercycle.sol.py').Eulercycle
        out = Eulercycle().eulercycle(sample['node'], sample['edge'])
        return out

    def compare(self, path, sample):
        edges = sample['edge']
        return (len(path) == len(edges) + 1 and
                sorted(toEdge(path)) == sorted([[min(i), max(i)] for i in edges]))
        self.debugPrint('>', sample)
        self.debugPrint('<', out)


Tester(debug=True).judge()
