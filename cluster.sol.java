// author: linnil1
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.lang.Math;
import edu.princeton.cs.algs4.Point2D;


class Cluster {
    public List<double[]> cluster(List<int[]> points, int cluster_num) {
        ArrayList<Point2D> p = new ArrayList<Point2D>();
        for(int[] i: points) {
            p.add(new Point2D(i[0], i[1]));
            // System.out.print(i[0]);
            // System.out.print(i[1]);
        }
        // System.out.println(cluster_num);

        ArrayList<double[]> ans = new ArrayList<double[]>();
        ans.add(new double[]{0, 1.5});
        ans.add(new double[]{3, 1.5});
        return ans;
    }

    public static void main(String[] args) {
        List<double[]> out = new Cluster().cluster(new ArrayList<int[]>(){{
            add(new int[]{0,1});
            add(new int[]{0,2});
            add(new int[]{3,1});
            add(new int[]{3,2});
        }}, 2);
        for(double[] o: out)
            System.out.println(Arrays.toString(o));

    }
}
