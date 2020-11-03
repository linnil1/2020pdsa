// author: linnil1
import java.util.List;
import java.util.ArrayList;
import java.lang.Math;
import edu.princeton.cs.algs4.GrahamScan;
import edu.princeton.cs.algs4.Point2D;


class Airport {
    public double airport(List<int[]> houses) {
        // Setup for convex
        double cx=0., cy=0.;
        Point2D[] points = new Point2D[houses.size()];
        for(int i=0; i < houses.size(); ++i) {
            cx += houses.get(i)[0];
            cy += houses.get(i)[1];
            points[i] = new Point2D(houses.get(i)[0], houses.get(i)[1]);
        }
        Point2D center = new Point2D(cx / houses.size(), cy /  houses.size());
        GrahamScan graham = new GrahamScan(points);

        // Find min distance
        double dis = Double.POSITIVE_INFINITY;
        Point2D oldp = null, firstp = null;
        for (Point2D p: graham.hull()) {
            if (oldp == null) {
                oldp = p;
                firstp = p;
                continue;
            }
            dis = Math.min(dis, Math.abs(Point2D.area2(oldp, center, p)) / oldp.distanceTo(p));
            oldp = p;
        }
        dis = Math.min(dis, Math.abs(Point2D.area2(oldp, center, firstp)) / oldp.distanceTo(firstp));

        return dis;
    }

    public static void main(String[] args) {
        System.out.println(new Airport().airport(new ArrayList<int[]>(){{
            add(new int[]{0,0});
            add(new int[]{1,0});
            add(new int[]{0,1});
        }}));
    }
}
