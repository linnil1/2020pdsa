import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.IOException;

import java.util.Arrays;
/*
dk openjdk:8-slim javac -cp gson.jar two_sum_judge.java  two_sum_sol.java
dk openjdk:8-slim java -cp gson.jar:. two_sum_judge
*/

public class two_sum_judge {
    static boolean compare(int[] out, Sample s) {
        return Arrays.equals(out, s.answer);
    }

    static int[] run(Sample s) {
        return new two_sum_sol().twoSum(s.nums, s.target);
        // return s.answer;
    }

    public static void main(String []args) {
        Gson gson = new Gson();
        try {
            Case[] cases = gson.fromJson(new FileReader("two_sum.json"), Case[].class);
            for(int i=0; i<cases.length; ++i) {
                Case c = cases[i];
                long times = 0;
                System.out.println("Score: " + String.valueOf(c.score));
                System.out.println("Case: " + String.valueOf(c.case_name));
                for(int j=0; j<c.data.length; ++j) {
                    Sample s = c.data[j];
                    long clk_s = System.currentTimeMillis();
                    int[] out = run(s);
                    clk_s = System.currentTimeMillis() - clk_s;

                    // System.out.print(clk_s);
                    // System.out.println(" ms");
                    times += clk_s;

                    if (!compare(out, s)) {
                        System.out.println("< " + Arrays.toString(out));
                        System.out.println("> " + Arrays.toString(s.answer));
                    }
                }
                System.out.println(String.valueOf(times) + " ms");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class Sample {
        int[] nums;
        int target;
        int[] answer;
        public Sample() {}
    }

    static class Case {
        @SerializedName("case")
        int case_name;
        int score;
        Sample[] data;
        public Case() {}
    }
}
