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
        if (i > j)
            return 1;
        return 0;
    }

    public static class ComparatorOfDistance implements Comparator<Restaurant> {
        public int compare(Restaurant a, Restaurant b) {
            if (a.distance != b.distance) {
                if (a.distance < b.distance)
                    return -1;
                else
                    return 1;
            }
            if (a.id > b.id)
                return -1;
            else
                return 1;
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

    public List<Restaurant> filter(int min_price, int max_price, int min_rate) {
        List<Restaurant> inds = new ArrayList<Restaurant>();
        for(Restaurant r: this.restaurants) {
            if (r.price > max_price)
                break;
            if (r.rate >= min_rate &&
                r.price >= min_price)
                inds.add(r);
        }
        return inds;
    }

    public static void main(String[] args) {
        // test
        List<Restaurant> restaurants = new ArrayList<Restaurant>();
        restaurants.add(new Restaurant(3, 1, 20, 12));
        restaurants.add(new Restaurant(0, 3, 20, 11));
        restaurants.add(new Restaurant(2, 4, 20, 12));
        restaurants.add(new Restaurant(1, 5, 20, 11));
        Restaurants r = new Restaurants(restaurants);
        List<Restaurant> a = r.filter(0, 20, 1);
        for (Restaurant i: a) {
            System.out.print(i.getID());
            System.out.print(" ");
        }
        System.out.println(" ");
        Collections.sort(a);
        for (Restaurant i: a) {
            System.out.print(i.getID());
            System.out.print(" ");
        }
        System.out.println(" ");
        a.sort(new Restaurant.ComparatorOfDistance());
        for (Restaurant i: a) {
            System.out.print(i.getID());
            System.out.print(" ");
        }
        System.out.println(" ");
    }
}
