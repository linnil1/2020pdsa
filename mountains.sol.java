import java.util.List;
import java.util.ArrayList;
import java.util.Queue;
import java.lang.Math;


class Mountains {
    public Mountains() {};

    public int mountains(List<int[]> mountain_height) {
        return 0;
    }

    public static void main(String[] args) {
        Mountains m = new Mountains();
        System.out.println(m.mountains(new ArrayList<int[]>(){{
            add(new int[]{ 0,  1,  2,  3,  4});
            add(new int[]{24, 23, 22, 21,  5});
            add(new int[]{12, 13, 14, 15, 16});
            add(new int[]{11, 17, 18, 19, 20});
            add(new int[]{10,  9,  8,  7,  6});
        }}));
        // 42
        System.out.println(m.mountains(new ArrayList<int[]>(){{
            add(new int[]{3,4,5});
            add(new int[]{9,3,5});
            add(new int[]{7,4,3});
        }}));
        // 6
    }
}
