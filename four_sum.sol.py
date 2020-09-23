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
        # For non-duplicate data N^2
        answer = []
        two_value_map = defaultdict(list)
        for i, a in enumerate(nums):
            for b in nums[i+1:]:
                two_value_map[a + b].append((a, b))

        for i in two_value_map.keys():
            if not two_value_map.get(target - i):
                continue
            for a in two_value_map[i]:
                for b in two_value_map[target - i]:
                    if b[0] != a[0] != b[1] != a[1] != b[0]:
                        answer.append(tuple(sorted([*a, *b])))

        return list(map(list, sorted(set(answer))))

        # N^3
        nums = sorted(nums)
        answer = []
        ind = set(nums)
        for i, a in enumerate(nums):
            if a + a + a + a >= target:
                break
            for j in range(i + 1, len(nums)):
                b = nums[j]
                if a + b + b + b >= target:
                    break
                for k in range(j + 1, len(nums)):
                    c = nums[k]
                    if a + b + c + c >= target:
                        break
                    if target - a - b - c in ind:
                        answer.append([a, b, c, target - a - b - c])
        return answer

        # For duplicated data N^2
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


# print(Solution().fourSum([1, 0, -1, -2, 2], 0))
