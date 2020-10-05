import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.IOException;

/*
dk openjdk:8-slim javac -cp gson.jar percolation_judge.java  percolation_sol.java
dk openjdk:8-slim java -cp gson.jar:. percolation_judge
*/

public abstract class Judger<Tout> {
    protected abstract boolean compare(Tout out, JsonElement s);

    protected abstract Tout run(JsonElement s);

    protected abstract void debugPrint(Tout out, JsonElement s);

    protected void judge(String file_json) {
        Gson gson = new Gson();
        try {
            Case[] cases = gson.fromJson(new FileReader(file_json), Case[].class);
            for(int i=0; i<cases.length; ++i) {
                Case c = cases[i];
                long times = 0;
                System.out.println("Score: " + String.valueOf(c.score));
                System.out.println("Case: " + String.valueOf(c.case_name));
                for(int j=0; j<c.data.size(); ++j) {
                    JsonElement s = c.data.get(j);
                    long clk_s = System.currentTimeMillis();
                    Tout out = run(s);

                    clk_s = System.currentTimeMillis() - clk_s;
                    times += clk_s;
                    System.out.println("\tSample" + String.valueOf(j) + ":\t" 
                                       + String.valueOf(clk_s) + "ms");

                    if (!compare(out, s))
                        debugPrint(out, s);
                }
                System.out.println("Total time:\t" + String.valueOf(times) + " ms");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class Case {
        @SerializedName("case")
        int case_name;
        int score;
        JsonArray data;
        public Case() {}
    }
}
