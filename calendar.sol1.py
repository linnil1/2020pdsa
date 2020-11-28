# author: linnil1
# use sortedcontainers
from sortedcontainers import SortedList


class Calendar:
    def __init__(self):
        self.mylist = SortedList()

    def book(self, start: int, end: int) -> bool:
        """
        Book the from start(included) to end(excluded)

        If availble: book it and return True
        else: return False
        If availble: book it.
        """
        assert start < end

        a = self.mylist.bisect_right(start)
        b = self.mylist.bisect_left(end)
        
        if a % 2 or a != b:
            return False

        self.mylist.add(start)
        self.mylist.add(end)
        return True
