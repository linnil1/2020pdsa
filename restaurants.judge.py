from Judger import Judger
import imp


class Tester(Judger): 
    def __init__(self):
        super().__init__("restaurants.json", debug=True)

    def run(self, sample):
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
            if out[i] != sample[1 + i]['answer']:
                # print('<', out)
                # print('>', sample[1 + i]['answer'])
                return False
        return True


Tester().judge()
#sample={'nums':[-1,0,1,2,3,4],'target':2}
#print(Tester().run(sample))
