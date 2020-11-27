from Judger import Judger
import sys
import numbers


class Tester(Judger): 
    def __init__(self, debug=True):
        if debug:
            super().__init__("cluster.json")
        else:
            super().__init__(sys.argv[1], debug=False, save=True, clean_after_read=True)

    def run(self, sample):
        import imp
        Cluster = imp.load_source("Cluster", 'cluster.sol.py').Cluster
        out = Cluster().cluster(sample['points'], sample['cluster_num'])
        return out

    def compare(self, out, sample):
        if type(out) is not list:
            return False
        sample = sample['answer']
        if len(out) != len(sample):
            return False
        for i in range(len(out)):
            if len(out[i]) != len(sample[i]):
                return False
            for j in range(len(out[i])):
                if not isinstance(out[i][j], numbers.Number):
                    return False
                if abs(out[i][j] - sample[i][j]) > 1e-3:
                    print('<', out)
                    print('>', sample)
                    return False
                return True


Tester(debug=True).judge()
# Tester(debug=True).judge()
