import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.lang.Math;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. calendar.sol.java calendar.judge.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<List<Boolean>> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "calendar.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        String func;
        int[] args;
        Boolean answer;
        public Data() {};
    }

    @Override protected boolean compare(List<Boolean> out, JsonElement ele) {
        Data[] d = this.gson.fromJson(ele, Data[].class);
        for(int i=1; i<d.length; ++i) {
            if (!d[i].answer.equals(out.get(i - 1)))
                return false;
        }
        return true;
    }

    @Override protected List<Boolean> run(JsonElement ele) {
        Data[] d = this.gson.fromJson(ele, Data[].class);
        ArrayList<Boolean> out = new ArrayList<Boolean>();
        this.resetTime();
        Calendar calendar = new Calendar();

        for(int i=1; i<d.length; ++i)
            out.add(calendar.book(d[i].args[0], d[i].args[1]));

        return out;
    }

    @Override protected void debugPrint(List<Boolean> out, JsonElement ele) {
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
