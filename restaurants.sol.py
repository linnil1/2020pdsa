import functools
from typing import List


class Restaurant(object):
    def __init__(self, id :int, rate :int, price :int, distance :int):
        self.id = id
        self.rate = rate
        self.price = price
        self.distance = distance

    def getID(self) -> int:
        return self.id

    def __lt__(self, b) -> bool:
        return self.price * self.distance *    b.rate < \
                  b.price *    b.distance * self.rate

    @staticmethod
    def comparator1(a, b) -> int:
        """
        Compare two restaurants by restaurant object

        The output should be in the increasing order of rate, if the rate is same,
        sorted by increasing order by distance, if both are same,
        order restaurants by id from highest to lowest.

        Parameters:
          a(Restaurant): The restaurant object
          b(Restaurant): The restaurant object

        Returns:
            result(int): -1 for restaurant a has smaller order, 1 for restaurant b has smaller order, 0 for equal.
        """
        a = (a.rate, a.distance, -a.id)
        b = (b.rate, b.distance, -b.id)
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0


class Restaurants(object):
    def __init__(self, restaurants :List[Restaurant]):
        """
        Init restaurants list 

        Parameters:
            restaurants (List[List[int]]): the list of restaurants
                each restaurant has five attributes in this order:
                id(int), rate(int), price(int), distance(int)

                Note: 1 <= rate <= 5
        """
        # sort restaurants
        self.restaurants = sorted(restaurants, key=lambda a: (a.rate, a.price))

        # Find rate levels
        self.rate = [0] * 7
        self.rate[6] = len(self.restaurants)
        now_rate = 1
        for i in range(self.rate[6]):
            while self.restaurants[i].rate != now_rate:
                now_rate += 1
                self.rate[now_rate] = i
        for i in range(now_rate + 1, 6):
            self.rate[i] = self.rate[6]
        # print(self.rate)

    def binary(self, s, e, p):
        while s < e:
            mid = (s + e) // 2
            if self.restaurants[mid].price >= p:
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

        Returns:
            restaurants (List[Restaurant]): The list of restaurant object.
        """
        # return []
        ids = []
        for r in range(min_rate, 6):
            pos_start = self.binary(self.rate[r], self.rate[r + 1], min_price)
            for i in range(pos_start, self.rate[r + 1]):
                if self.restaurants[i].price <= max_price:
                    ids.append(i)
                else:
                    break

        ids.sort(key=lambda i: (self.restaurants[i].distance, -self.restaurants[i].id))
        return [self.restaurants[i].id for i in ids]


if __name__ == "__main__":
    rests = [
        # id, rate, price, distance
        Restaurant(20, 1, 20, 12),
        Restaurant(15, 3, 19, 11),
        Restaurant(19, 4, 19, 12),
        Restaurant(18, 5, 20, 11),
    ]
    r = Restaurants(rests)
    print(r.filter(0, 25, 3)) 
    print(r.filter(0, 25, 4)) 
    print(r.filter(0, 20, 1)) 
    print(r.filter(0, 10, 1))
    print(r.filter(0, 19, 1))
    print(r.filter(19, 19, 3))

    # case6
    rests = [
        # id, rate, price, distance
        Restaurant(3, 2, 3, 8),
        Restaurant(0, 2, 4, 6),
        Restaurant(2, 4, 5, 12),
        Restaurant(1, 5, 6, 11),
    ]
    print([i.getID() for i in sorted(rests)])
    print([i.getID() for i in sorted(rests, key=functools.cmp_to_key(Restaurant.comparator1))])

    """
Output:
[18, 15, 19]
[18, 19]
[18, 15, 20, 19]
[]
[15, 19]
[15, 19]
[3, 0, 1, 2]
[0, 3, 2, 1]
    """

