import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.IOException;


public abstract class Judger<Tout> {
    protected abstract boolean compare(Tout out, JsonElement s);

    protected abstract Tout run(JsonElement s);

    protected abstract void debugPrint(Tout out, JsonElement s);

    protected Gson gson;
    protected long runtime_acc;
    protected long runtime_from;

    public Judger() {
        this.gson = new Gson();
    }

    protected void initTime() {
        this.runtime_acc = 0;
        this.resetTime();
    }

    protected void resetTime() {
        this.runtime_from = System.currentTimeMillis();
    }

    protected void updateTime() {
        this.runtime_acc += System.currentTimeMillis() - this.runtime_from;
        this.resetTime();
    }

    protected void judge(String file_json) {
        try {
            Case[] cases = this.gson.fromJson(new FileReader(file_json), Case[].class);
            for(int i=0; i<cases.length; ++i) {
                Case c = cases[i];
                long times = 0;
                System.out.println("Score: " + String.valueOf(c.score));
                System.out.println("Case: " + String.valueOf(c.case_name));
                for(int j=0; j<c.data.size(); ++j) {
                    JsonElement s = c.data.get(j);

                    this.initTime();
                    Tout out = run(s);
                    this.updateTime();

                    System.out.print("\tSample" + String.valueOf(j) + ":\t");
                    if (!compare(out, s)) {
                        debugPrint(out, s);
                        System.out.print("WA");
                    }
                    else
                        System.out.print("AC");

                    times += this.runtime_acc;
                    System.out.println("\t" + String.valueOf(this.runtime_acc) + "ms");

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
