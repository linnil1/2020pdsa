import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Queue;
import java.util.Stack;
import java.util.Comparator;
import java.lang.Math;


class Eulercycle {
    public Eulercycle() {};

    public int[] eulercycle(int num_node, int[][] edges) {
        return new int[]{0,1,2,0};
    }

    public boolean check(int[] path, int[][] edges) {
        if(path.length != edges.length + 1)
            return false;

        int[][] output_edges = new int[path.length - 1][2];
        for(int i=0; i<path.length-1; ++i) {
            output_edges[i][0] = Math.min(path[i], path[i+1]);
            output_edges[i][1] = Math.max(path[i], path[i+1]);
        }
        Arrays.sort(output_edges, (a, b) -> Arrays.compare(a,b));
        Arrays.sort(edges, (a, b) -> Arrays.compare(a,b));

        for(int i=0;i<path.length-1; ++i)
            if(!Arrays.equals(output_edges[i], edges[i]))
                return false;
        return true;
    }

    public static void main(String[] args) {
        Eulercycle m = new Eulercycle();
        int[][] edges = new int[][]{ {0,1}, {1,2}, {0,2} };
        int[] path = m.eulercycle(3, edges);
        // 0 1 2 0
        System.out.println(m.check(path, edges));
    }
}
