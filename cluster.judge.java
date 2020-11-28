import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.lang.Math;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. cluster.sol.java cluster.judge.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<List<double[]>> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "cluster.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        List<int[]> points;
        int cluster_num;
        List<double[]> answer;
        public Data() {};
    }

    @Override protected boolean compare(List<double[]> out, JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        if(out.size() != d.answer.size())
            return false;
        for(int i=0; i<out.size(); ++i) {
            if (Math.abs(d.answer.get(i)[0] - out.get(i)[0]) > 1e-3)
                return false;
            if (Math.abs(d.answer.get(i)[1] - out.get(i)[1]) > 1e-3)
                return false;
        }
        return true;
    }

    @Override protected List<double[]> run(JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        this.resetTime();
        return new Cluster().cluster(d.points, d.cluster_num);
    }

    @Override protected void debugPrint(List<double[]> out, JsonElement ele) {
        // System.out.println("<" + Double.toString(out));
        // System.out.println(">" + Double.toString(this.gson.fromJson(ele, Data.class).answer));
        // System.out.println(">" + gson.toJson(ele));
    };

    public static void main(String []args) {
        // Judge j = new Judge(false, true);
        Judge j = new Judge(true, false);
        j.judge(args);
    }
}
