import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;


public abstract class Judger<Tout> {
    protected abstract boolean compare(Tout out, JsonElement s);

    protected abstract Tout run(JsonElement s);

    protected abstract void debugPrint(Tout out, JsonElement s);

    protected Gson gson;

    private long runtime_acc, runtime_from;
    private boolean debug;
    protected boolean clean_after_read;
    protected String file_path;

    public Judger() {
        this(true);
    }

    public Judger(boolean debug) {
        this.gson = new Gson();
        this.debug = debug;
        this.clean_after_read = false;
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

    protected void judge(String[] args) {
        if (args.length > 0)
            this.judge(args[0]);
        else {
            this.debug = true;
            this.judge(this.file_path);
        }
    }

    protected void judge(String file_json) {
        try {
            // run all case
            Case[] cases = this.gson.fromJson(new FileReader(file_json), Case[].class);
            if (this.clean_after_read && !this.debug) {
                FileWriter fout = new FileWriter(file_json);
                fout.flush();
                fout.close();
            }
            for(int i=0; i<cases.length; ++i) {
                Case c = cases[i];
                Status[] status = new Status[c.data.size()];
                // run all sample
                for(int j=0; j<c.data.size(); ++j) {
                    JsonElement ele = c.data.get(j);

                    this.initTime();
                    Tout out = run(ele);
                    this.updateTime();

                    status[j] = new Status();
                    status[j].time = this.runtime_acc;
                    if (!compare(out, ele)) {
                        this.debugPrint(out, ele);
                        status[j].status = "WA";
                    }
                    else
                        status[j].status = "AC";
                }

                // output all sample
                if (this.debug) {
                    System.out.println("Case: " + String.valueOf(c.case_name));
                    boolean is_ac = true;
                    long times = 0;
                    for(int j=0; j<c.data.size(); ++j) {
                        if (status[j].status != "AC")
                            is_ac = false;
                        times += status[j].time;
                        System.out.print("\tSample" + String.valueOf(j) + ":\t" + status[j].status);
                        System.out.println("\t" + String.valueOf(status[j].time) + "ms");
                    }
                    if (is_ac)
                        System.out.println("Score:\t" + String.valueOf(c.score) + "/" + String.valueOf(c.score));
                    else
                        System.out.println("Score:\t0/" + String.valueOf(c.score));
                    System.out.println("Total time:\t" + String.valueOf(times) + " ms");
                } else {
                    // not debug => write to file
                    FileWriter fout = new FileWriter("case" + String.valueOf(c.case_name) + ".out");
                    this.gson.toJson(status, fout);
                    fout.flush();
                    fout.close();
                }
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

    static class Status {
        long time;
        String status;
        public Status() {
            this.time = 0;
            this.status = "RE";
        }
    }
}
