import json
import imp
import time
from pprint import pprint


class Judger:
    def __init__(self, name="data.json", debug=False):
        self.name = name
        self.debug = debug

    def debugPrint(self, *args, pretty=False):
        if self.debug:
            if pretty:
                pprint(*args)
            else:
                print(*args)

    def judgeCase(self, case):
        output = []

        for sample in case:
            now = {}

            # main run
            clk_s = time.time()
            try:
                out = self.run(sample)
                now['time'] = (time.time() - clk_s) * 1000
            except Exception as e:
                now['time'] = (time.time() - clk_s) * 1000
                now["status"] = 'RE'
                output.append(now)
                lbjtdln5
                continue

            # compare
            if not self.compare(out, sample):
                now['status'] = "WA"
            else:
                now['status'] = "AC"

            output.append(now)

        return output

    def judge(self):
        data = json.load(open(self.name))
        scores = {}
        for case in data:
            casename = f"case{case['case']}"
            self.debugPrint("Case:", casename)

            case_output = self.judgeCase(case['data'])
            times = sum(i['time'] for i in case_output)
            isAC = all(i['status'] == "AC" for i in case_output)
            score = case['score'] if isAC else 0
            scores[casename] = score

            for i, co in enumerate(case_output):
                self.debugPrint(f"\tSample{i}:\t{co['status']}\t{co['time']:.2f}ms")
            self.debugPrint(f"Score: {score} / {case['score']}")
            self.debugPrint(f"Total: {times:.2f}ms")

        self.debugPrint(json.dumps({'scores': scores}))

    def run(self, sample):
        return 0

    def compare(self, out, sample):
        return True
