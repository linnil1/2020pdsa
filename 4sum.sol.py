from typing import List
from collections import defaultdict


class Solution:
    def compare(self, count_dict, a, b):
        ans = tuple(sorted([*a, *b]))
        c = None
        v = 0
        for i in ans:
            if c == i:
                v += 1
            else:
                if v > 1 and c is not None and v > count_dict[c]:
                    return False
                c = i
                v = 1
        if c is not None and v > count_dict[c]:
            return False
        return ans

    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        count_dict = defaultdict(int)
        answer = []
        for v in nums:
            count_dict[v] += 1

        two_value_map = defaultdict(list)

        num = []
        for i in sorted(count_dict.keys()):
            num.append(i)
            for j in num:
                if i == j and count_dict[i] < 2:
                    continue
                two_value_map[i + j].append((j, i))

        for i in two_value_map.keys():
            if not two_value_map.get(target - i):
                continue
            for a in two_value_map[i]:
                for b in two_value_map[target - i]:
                    if ans := self.compare(count_dict, a, b):
                        answer.append(ans)

        oldanswer = sorted(answer)
        answer = []
        for a in oldanswer: 
            if not answer:
                answer.append(a)
            elif a != answer[-1]:
                answer.append(a)
        return list(map(list, answer))
