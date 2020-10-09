// author: linnil1
// Brute force
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Comparator;
import java.util.Collection;

class Restaurants {
    private List<int[]> restaurants;

    public Restaurants(List<int[]> restaurants) {
        this.restaurants = restaurants;
        this.restaurants.sort(new Comparator<int[]>() {
            @Override
            public int compare(int[] a, int[] b) {
                // id(int), rate(int), price(int), distance(int)
                if (a[2] != b[2]) {
                    if (a[2] < b[2])
                        return -1;
                    else if (a[2] > b[2])
                        return 1;
                }
                return 0;
            }
        });
    }

    public int[] filter(int max_price, int min_rate) {
        // return new int[]{};
        List<Integer> inds = new ArrayList<Integer>();
        // for(int i=0; i<this.restaurants.size(); ++i)
        //     if (this.restaurants.get(i)[1] >= min_rate && this.restaurants.get(i)[2] <= max_price)
        for(int i=0; i<this.restaurants.size() && this.restaurants.get(i)[2] <= max_price; ++i)
            if (this.restaurants.get(i)[1] >= min_rate)
                inds.add(i);

        inds.sort(new Comparator<Integer>() {
            @Override
            public int compare(Integer i, Integer j) {
                // id(int), rate(int), price(int), distance(int)
                int[] a = restaurants.get(i);
                int[] b = restaurants.get(j);
                if (a[3] != b[3]) {
                    if (a[3] < b[3])
                        return -1;
                    else if (a[3] > b[3])
                        return 1;
                }
                else if (a[0] > b[0])
                    return -1;
                else if (a[0] < b[0])
                    return 1;
                return 0;
            }
        });

        int[] ids = new int[inds.size()];
        for(int i=0; i<inds.size(); ++i)
            ids[i] = this.restaurants.get(inds.get(i))[0];
        return ids;
    }

    public static void main(String[] args) {
        // test
        List<int[]> restaurants = new ArrayList<int[]>();
        restaurants.add(new int[]{20, 1, 20, 12});
        restaurants.add(new int[]{15, 3, 20, 11});
        restaurants.add(new int[]{19, 4, 20, 12});
        restaurants.add(new int[]{18, 5, 20, 11});
        Restaurants g = new Restaurants(restaurants);
        System.out.println(Arrays.toString(g.filter(25, 3)));
        System.out.println(Arrays.toString(g.filter(25, 4)));
        System.out.println(Arrays.toString(g.filter(20, 1)));
        System.out.println(Arrays.toString(g.filter(10, 1)));
    }
}
