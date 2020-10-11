from typing import List


class Restaurants(object):
    def __init__(self, restaurants :List[List[int]]):
        """
        Init restaurants list 

        Parameters:
            restaurants (List[List[int]]): the list of restaurants
                each restaurant has five attributes in this order:
                id(int), rate(int), price(int), distance(int)

                Note: 1 <= rate <= 5
        """
        self.restaurants = sorted(restaurants, key=lambda a: (a[1], a[2]))
        self.rate = [0] * 7
        self.rate[6] = len(self.restaurants)
        now_rate = 1
        for i in range(self.rate[6]):
            while self.restaurants[i][1] != now_rate:
                now_rate += 1
                self.rate[now_rate] = i
        for i in range(now_rate + 1, 6): 
            self.rate[i] = self.rate[6]
        # print(self.rate)

    def binary(self, s, e, p):
        while s < e:
            mid = (s + e) // 2
            if self.restaurants[mid][2] >= p:
                e = mid
            elif mid == s:
                break
            else:
                s = mid
        return e


    def filter(self, min_price: int, max_price :int, min_rate: int):
        """
        Filter the restaurants list

        You should output the id of restaurants that meets the condition:
        `min_price <= price <= max_price` and `rate >= min_rate`.

        The output should be in the increasing order of distance, if the distance is same,
        order restaurants by id from highest to lowest.
        
        Returns:
            restaurant_ids (List[int]): The id of restaurants.
        """
        # return []
        ids = []
        for r in range(min_rate, 6):
            pos_start = self.binary(self.rate[r], self.rate[r + 1], min_price)
            # print(self.rate[r], pos_end)
            v = pos_start
            for i in range(pos_start, self.rate[r + 1]):
                if self.restaurants[i][2] <= max_price:
                    ids.append(i)
                else:
                    break

        # ids = [i for i, res in enumerate(self.restaurants) if res[1] >= min_rate and res[2] <= max_price]
        # ids = [i + self.rate[min_rate] for i, res in enumerate(self.restaurants[self.rate[min_rate]:]) if res[2] <= max_price]
        # ids = filter(lambda res: res[2] <= max_price, self.restaurants[self.rate[min_rate]:])
        # return [i[0] for i in sorted(ids, key=lambda res: (res[3], -res[0]))]

        ids = sorted(ids, key=lambda i: (self.restaurants[i][3], -self.restaurants[i][0]))
        return [self.restaurants[i][0] for i in ids]


if __name__ == "__main__":
    r = Restaurants([
        # id, rate, price, distance
        [20, 1, 20, 12],
        [15, 3, 19, 11],
        [19, 5, 19, 12],
        [18, 5, 20, 11],
        ])
    print(r.filter(0, 25, 3))
    print(r.filter(0, 25, 4))
    print(r.filter(0, 20, 1))
    print(r.filter(0, 10, 1))
    print(r.filter(0, 19, 1))
    print(r.filter(20, 20, 1))
