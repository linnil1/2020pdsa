// author: linnil1
import java.util.List;
import java.util.ArrayList;
import java.util.Queue;
import java.lang.Math;


class Railway {
    public Railway() {};

    public int railway(int landmarks, List<int[]> distance) {
        return 10000;
    }

    public static void main(String[] args) {
        Railway team = new Railway();
        System.out.println(team.railway(4, new ArrayList<int[]>(){{
            add(new int[]{0,1,2});
            add(new int[]{0,2,4});
            add(new int[]{1,3,5});
            add(new int[]{2,1,1});
        }}));
        System.out.println(team.railway(4, new ArrayList<int[]>(){{
            add(new int[]{0,1,0});
            add(new int[]{0,2,4});
            add(new int[]{0,3,4});
            add(new int[]{1,2,1});
            add(new int[]{1,3,4});
            add(new int[]{2,3,2});
        }}));
    }
}
