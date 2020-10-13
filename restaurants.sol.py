import functools
from typing import List, NewType

class Restaurant(object):
    def __init__(self, id, rate, price, distance):
        self.id = id
        self.rate = rate
        self.price = price
        self.distance = distance

    def __lt__(self, b):
        return self.price * self.distance *    b.rate < \
                  b.price *    b.distance * self.rate

    @staticmethod
    def comparatorOfDistance(a, b):
        """
        Compare two restaurants by restaurant's id.

        The output should be in the increasing order of distance, if the distance is same,
        order restaurants by id from highest to lowest.

        Parameters:
          a(Restaurant): The restaurant object
          b(Restaurant): The restaurant object
        
        Returns:
            result(int): -1 for restaurant a has smaller order, 1 for restaurant b has smaller order, 0 for equal.
        """
        a = (a.distance, -a.id)
        b = (b.distance, -b.id)
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
        rests = []
        for r in range(min_rate, 6):
            pos_start = self.binary(self.rate[r], self.rate[r + 1], min_price)
            for i in range(pos_start, self.rate[r + 1]):
                if self.restaurants[i].price <= max_price:
                    rests.append(self.restaurants[i])
                else:
                    break

        return rests


if __name__ == "__main__":
    r = Restaurants([
        # id, rate, price, distance
        Restaurant(3, 1, 20, 12),
        Restaurant(0, 3, 20, 11),
        Restaurant(2, 4, 20, 12),
        Restaurant(1, 5, 20, 11),
    ])
    a = r.filter(0, 20, 1)
    print([i.id for i in a])
    a.sort()
    print([i.id for i in a])
    a.sort(key=functools.cmp_to_key(Restaurant.comparatorOfDistance))
    print([i.id for i in a])
