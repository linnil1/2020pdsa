from Judger import Judger
import imp


class Tester(Judger): 
    def __init__(self):
        super().__init__("percolation.json", debug=True)

    def run(self, sample):
        Percolation = imp.load_source("Percolation", 'percolation.sol.py').Percolation
        s = Percolation(*sample[0]['args'])
        out = []
        for sam in sample[1:]:
            o = getattr(s, sam['func'])(*sam['args'])
            if sam['answer'] is not None:
                out.append(o)
        return out

    def compare(self, out, sample):
        ans = [sam['answer'] for sam in sample[1:] if sam['answer'] is not None]
        if ans == out:
            return True
        else:
            print('<', out)
            print('>', ans)
            return False


Tester().judge()
#sample={'nums':[-1,0,1,2,3,4],'target':2}
#print(Tester().run(sample))
