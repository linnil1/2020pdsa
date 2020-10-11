from typing import List


class Warriors: 
    def warriors1(self, strength :List[int], attack_range :List[int]):
        N = len(strength)
        if N != len(attack_range):
            raise ValueError
        attack_interval = [0] * 2 * N
        stack = [0] * N
        now = 0
        for i in range(N + 1):
            while now and (i == N or strength[stack[now-1]] <= strength[i]):
                id = stack[now - 1]
                now -= 1
                attack_interval[id * 2 + 1] = min(id + attack_range[id], i - 1)
            stack[now] = i
            now += 1

        now = 0
        for i in range(N - 1, -2, -1):
            while now and (i == -1 or strength[stack[now-1]] <= strength[i]):
                id = stack[now - 1]
                now -= 1
                attack_interval[id * 2] = max(id - attack_range[id], i + 1)
            stack[now] = i
            now += 1


        return attack_interval

    def warriors(self, strength :List[int], attack_range :List[int]):
        """
        Given the attributes of each warriors and output the minimal and maximum
        index of warrior can be attacked by each warrior.

        Parameters:
          strength (List[int]): The strength value of N warriors
          attack_range (List[int]): The range value of N warriors

        Returns:
          attack_interval (List[int]):
              The min and the max index that the warrior can attack.
              The format of output is 2N int array `[a0, b0, a1, b1, ...]`
        """
        N = len(strength)
        if N != len(attack_range):
            raise ValueError
        attack_interval = [0] * 2 * N
        stack = []
        for i in range(N + 1):
            while len(stack) and (i == N or strength[stack[-1]] <= strength[i]):
                id = stack.pop()
                attack_interval[id * 2 + 1] = min(id + attack_range[id], i - 1)
            stack.append(i)

        stack = []
        for i in range(N - 1, -2, -1):
            while len(stack) and (i == -1 or strength[stack[-1]] <= strength[i]):
                id = stack.pop()
                attack_interval[id * 2] = max(id - attack_range[id], i + 1)
            stack.append(i)

        """
        for i in range(N):
            id = i * 2
            if attack_interval[id] == i:
                attack_interval[id] = min(attack_interval[id] + 1, attack_interval[id + 1])
            if attack_interval[id + 1] == i:
                attack_interval[id + 1] = max(attack_interval[id], attack_interval[id + 1] - 1)
            if attack_interval[id] == i == attack_interval[id + 1]:
                attack_interval[id] = attack_interval[id + 1] = -1
        """
        return attack_interval


if __name__ == "__main__":
    sol = Warriors()
    print(sol.warriors([11, 13, 11, 7, 15],
                       [ 1,  8,  1, 7,  2]))
    """
    # Output
    [0, 0, 0, 3, 2, 3, 3, 3, 2, 4]
    """
