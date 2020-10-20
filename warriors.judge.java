import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. warriors.judge.java warriors.sol.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<int[]> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "warriors.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        int[] strength;
        int[] attack_range;
        int[] answer;
        public Data() {};
    }

    @Override protected boolean compare(int[] out, JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        return Arrays.equals(d.answer, out);
    }

    @Override protected int[] run(JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        this.resetTime();
        return new Warriors().warriors(d.strength, d.attack_range);
    }

    @Override protected void debugPrint(int[] out, JsonElement ele) {
        // System.out.println("<" + Arrays.toString(out));
        // System.out.println(">" + gson.toJson(ele));
    };

    public static void main(String []args) {
        // Judge j = new Judge(false, true);
        Judge j = new Judge(true, false);
        j.judge(args);
    }
}
