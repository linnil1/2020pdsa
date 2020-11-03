import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.lang.Math;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. airport.sol.java airport.judge.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<Double> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "airport.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        List<int[]> houses;
        double answer;
        public Data() {};
    }

    @Override protected boolean compare(Double out, JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        return Math.abs(d.answer - out) <= 1e-4;
    }

    @Override protected Double run(JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        this.resetTime();
        return new Airport().airport(d.houses);
    }

    @Override protected void debugPrint(Double out, JsonElement ele) {
        System.out.println("<" + Double.toString(out));
        System.out.println(">" + Double.toString(this.gson.fromJson(ele, Data.class).answer));
        // System.out.println(">" + gson.toJson(ele));
    };

    public static void main(String []args) {
        // Judge j = new Judge(false, true);
        Judge j = new Judge(true, false);
        j.judge(args);
    }
}
