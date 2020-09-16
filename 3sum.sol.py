from typing import List
from collections import defaultdict 


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        count_dict = defaultdict(int)
        answer = []
        for i, v in enumerate(nums):
            count_dict[v] += 1
        num = list(sorted(count_dict.keys()))
        for ind_i, i in enumerate(num):
            if i > 0:
                break
            for j in num[ind_i:]:
                target = 0 - i - j
                if target < j:
                    break
                if i == j and count_dict[i] <= 1:
                    continue
                if j == target and count_dict[j] <= 1:
                    continue
                if i == j == target and count_dict[i] <= 2:
                    continue
                if not count_dict.get(target):
                    continue
                answer.append([i, j, target])
        return answer
