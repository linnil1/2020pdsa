from typing import List
from collections import defaultdict


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # NlgN
        def binary(nums, target):
            a, b = 0, len(nums)
            while True:
                now = (a + b) // 2
                if nums[now] < target:
                    a = now
                elif nums[now] > target:
                    b = now
                else:
                    return now
                if a == b - 1:
                    return -1

        nums, ind = zip(*sorted(zip(nums, range(len(nums)))))
        for i in range(0, len(nums)):
            c = binary(nums, target - nums[i])
            if c != -1 and ind[c] != ind[i]:
                if ind[c] < ind[i]:
                    return [ind[c], ind[i]]
                else:
                    return [ind[i], ind[c]]
        return [0, 0]

        # N2
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]

        # N -> fast solution
        ind_dict = {}
        for i, num in enumerate(nums):
            if target - num in ind_dict:
                return [ind_dict[target - num], i]
            else:
                ind_dict[num] = i

        """
        # 1st solution
        num_dict = defaultdict(list)
        for i, v in enumerate(nums):
            num_dict[v].append(i)

        for key in num_dict:
            if key + key <= target and num_dict.get(target - key):
                if key + key == target:
                    if len(num_dict[key]) == 2:
                        return [num_dict[key][0], num_dict[key][1]]
                    elif len(num_dict[key]) > 2:
                        print("NOT OK")
                else:
                    if len(num_dict[key]) == 1 and len(num_dict[target - key]) == 1:
                        if num_dict[key][0] < num_dict[target - key][0]:
                            return [num_dict[key][0], num_dict[target - key][0]]
                        else:
                            return [num_dict[target - key][0], num_dict[key][0]]
                    else:
                        print("NOT OK")
        print("NOT OK")
        """
