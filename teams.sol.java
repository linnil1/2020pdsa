// author: linnil1
import java.util.List;
import java.util.ArrayList;
import java.util.Queue;
import java.lang.Math;


class Teams {
    public Teams() {};

    public boolean teams(int idols, List<int[]> teetee) {
        return true;
    }

    public static void main(String[] args) {
        Teams team = new Teams();
        System.out.println(team.teams(4, new ArrayList<int[]>(){{
            add(new int[]{0,1});
            add(new int[]{0,3});
            add(new int[]{2,1});
            add(new int[]{3,2});
        }}));
        System.out.println(team.teams(4, new ArrayList<int[]>(){{
            add(new int[]{0,1});
            add(new int[]{0,3});
            add(new int[]{2,1});
            add(new int[]{3,2});
            add(new int[]{0,2});
        }}));
    }
}
