import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.lang.Math;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. railway.sol.java railway.judge.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<Integer> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "railway.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        List<int[]> distance;
        int landmarks;
        Integer answer;
        public Data() {};
    }

    @Override protected boolean compare(Integer out, JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        return d.answer.equals(out);
    }

    @Override protected Integer run(JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        this.resetTime();
        return new Railway().railway(d.landmarks, d.distance);
    }

    @Override protected void debugPrint(Integer out, JsonElement ele) {
        System.out.print(">");
        System.out.println(this.gson.fromJson(ele, Data.class).answer);
        System.out.print("<");
        System.out.println(out);
    };

    public static void main(String []args) {
        // Judge j = new Judge(false, true);
        Judge j = new Judge(true, false);
        j.judge(args);
    }
}
