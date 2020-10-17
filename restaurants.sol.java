// author: linnil1
// Brute force
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Comparator;
import java.util.Collections;


class Restaurant implements Comparable<Restaurant> {
    public int id, rate, price, distance;
    Restaurant(int id, int rate, int price, int distance) {
        this.id = id;
        this.rate = rate;
        this.price = price;
        this.distance = distance;
    }

    public int getID() {
        return this.id;
    }

    @Override
    public int compareTo(Restaurant b) {
        int i = this.price * this.distance *    b.rate,
            j =    b.price *    b.distance * this.rate;
        if (i < j)
            return -1;
        else if (i > j)
            return 1;
        return 0;
    }

    public static class Comparator1 implements Comparator<Restaurant> {
        public int compare(Restaurant a, Restaurant b) {
            if (a.rate != b.rate) {
                if (a.rate < b.rate)
                    return -1;
                else
                    return 1;
            }
            if (a.distance != b.distance) {
                if (a.distance < b.distance)
                    return -1;
                else
                    return 1;
            }
            if (a.id > b.id)
                return -1;
            else if (a.id < b.id)
                return 1;
            return 0;
        }
    }

    public static class ComparatorOfRatePrice implements Comparator<Restaurant> {
        public int compare(Restaurant a, Restaurant b) {
            if (a.price != b.price) {
                if (a.price < b.price)
                    return -1;
                else
                    return 1;
            }
            return 0;
        }
    }
}


class Restaurants {
    private List<Restaurant> restaurants;

    public Restaurants(List<Restaurant> restaurants) {
        this.restaurants = restaurants;
        this.restaurants.sort(new Restaurant.ComparatorOfRatePrice());
    }

    public int[] filter(int min_price, int max_price, int min_rate) {
        List<Integer> inds = new ArrayList<Integer>();
        for(int i=0; i < this.restaurants.size(); ++i) {
            if (this.restaurants.get(i).price > max_price)
                break;
            if (this.restaurants.get(i).rate >= min_rate &&
                this.restaurants.get(i).price >= min_price)
                inds.add(i);
        }
        Collections.sort(inds, new Comparator<Integer>() {
            @Override
            public int compare(Integer i, Integer j) {
                // id(int), rate(int), price(int), distance(int)
                Restaurant a = restaurants.get(i),
                           b = restaurants.get(j);
                if (a.distance != b.distance) {
                    if (a.distance < b.distance)
                        return -1;
                    else if (a.distance > b.distance)
                        return 1;
                }
                else if (a.id > b.id)
                    return -1;
                else if (a.id < b.id)
                    return 1;
                return 0;
            }
        });

        int[] ids = new int[inds.size()];
        for(int i=0; i<inds.size(); ++i)
            ids[i] = this.restaurants.get(inds.get(i)).getID();
        return ids;
    }

    public static void main(String[] args) {
        // test
        List<Restaurant> restaurants = new ArrayList<Restaurant>();
        restaurants.add(new Restaurant(20, 1, 20, 12));
        restaurants.add(new Restaurant(15, 3, 19, 11));
        restaurants.add(new Restaurant(19, 4, 19, 12));
        restaurants.add(new Restaurant(18, 5, 20, 11));
        Restaurants r = new Restaurants(restaurants);
        System.out.println(Arrays.toString(r.filter(0, 25, 3)));
        System.out.println(Arrays.toString(r.filter(0, 25, 4)));
        System.out.println(Arrays.toString(r.filter(0, 20, 1)));
        System.out.println(Arrays.toString(r.filter(0, 10, 1)));
        System.out.println(Arrays.toString(r.filter(0, 19, 1)));
        System.out.println(Arrays.toString(r.filter(19, 19, 3)));

        // case6
        restaurants = new ArrayList<Restaurant>();
        restaurants.add(new Restaurant(3, 2, 3, 8));
        restaurants.add(new Restaurant(0, 2, 4, 6));
        restaurants.add(new Restaurant(2, 4, 5, 12));
        restaurants.add(new Restaurant(1, 5, 6, 11));

        Collections.sort(restaurants);
        for (Restaurant a: restaurants) {
            System.out.print(a.getID());
            System.out.print(" ");
        }
        System.out.println("");

        Collections.sort(restaurants, new Restaurant.Comparator1());
        for (Restaurant a: restaurants) {
            System.out.print(a.getID());
            System.out.print(" ");
        }
        System.out.println("");
        /*
Output:
[18, 15, 19]
[18, 19]
[18, 15, 20, 19]
[]
[15, 19]
[15, 19]
[3, 0, 1, 2]
[0, 3, 2, 1]
        */

    }
}
