import json
import imp
import time
from pprint import pprint


class Judger:
    def __init__(self, name="data.json", debug=True,
                 save=False, clean_after_read=False):
        self.data_path = name
        self.debug = debug
        self.save = save
        self.clean_after_read = clean_after_read

    def debugPrint(self, *args, pretty=False):
        if self.debug:
            if pretty:
                pprint(*args)
            else:
                print(*args)

    def judgeCase(self, case):
        status = []

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
                status.append(now)
                continue

            # compare
            if not self.compare(out, sample):
                now['status'] = "WA"
            else:
                now['status'] = "AC"

            status.append(now)

        return status

    def judge(self):
        data = json.load(open(self.data_path))
        if self.clean_after_read:
            open(self.data_path, "w").close()

        scores = {}
        for case in data:
            casename = f"case{case['case']}"
            self.debugPrint("Case:", casename)

            case_status = self.judgeCase(case['data'])
            times = sum(i['time'] for i in case_status)
            isAC = all(i['status'] == "AC" for i in case_status)
            score = case['score'] if isAC else 0
            scores[casename] = score

            for i, co in enumerate(case_status):
                self.debugPrint(f"\tSample{i}:\t{co['status']}\t{co['time']:.2f}ms")
            self.debugPrint(f"Score: {score} / {case['score']}")
            self.debugPrint(f"Total: {times:.2f}ms")

            if self.save:
                json.dump(case_status, open(casename + ".out", "w"))

        self.debugPrint(json.dumps({'scores': scores}))

    def run(self, sample):
        return 0

    def compare(self, out, sample):
        return True
