import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.lang.Math;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. teams.sol.java teams.judge.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<Boolean> {

    public Judge(boolean debug, boolean clean_after_read) {
        super(debug);
        this.file_path = "teams.json";
        this.clean_after_read = clean_after_read;
    }

    static class Data {
        List<int[]> teetee;
        int idols;
        Boolean answer;
        public Data() {};
    }

    @Override protected boolean compare(Boolean out, JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        return d.answer.equals(out);
    }

    @Override protected Boolean run(JsonElement ele) {
        Data d = this.gson.fromJson(ele, Data.class);
        this.resetTime();
        return new Teams().teams(d.idols, d.teetee);
    }

    @Override protected void debugPrint(Boolean out, JsonElement ele) {
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
