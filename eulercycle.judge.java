import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.lang.Math;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. eulercycle.sol.java eulercycle.judge.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<int[]> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "eulercycle.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        int[][] edge;
        int node;
        public Data() {};
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

    @Override protected boolean compare(int[] out, JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        return this.check(out, d.edge);
    }

    @Override protected int[] run(JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        this.resetTime();
        return new Eulercycle().eulercycle(d.node, d.edge);
    }

    @Override protected void debugPrint(int[] out, JsonElement ele) {
        System.out.print(">");
        // System.out.println(this.gson.fromJson(ele, Data.class).answer);
        System.out.print("<");
        // System.out.println(out);
    };

    public static void main(String []args) {
        // Judge j = new Judge(false, true);
        Judge j = new Judge(true, false);
        j.judge(args);
    }
}
