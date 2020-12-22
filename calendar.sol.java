// author: linnil1
import java.util.List;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.lang.Math;
import edu.princeton.cs.algs4.Point2D;


class Calendar {
    public Calendar() {};

    public boolean book(int start, int end) {
        System.out.println(start);
        System.out.println(end);
        return true;
    }

    public static void main(String[] args) {
        Calendar calendar = new Calendar();
        System.out.println(calendar.book(0, 5));
    }
}
