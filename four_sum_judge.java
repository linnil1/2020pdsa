import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.IOException;

import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.util.Comparator;
/*
dk openjdk:8-slim javac -cp gson.jar two_sum_judge.java  two_sum_sol.java
dk openjdk:8-slim java -cp gson.jar:. two_sum_judge
*/

public class four_sum_judge {
    public static boolean compare(List<int[]> out, List<int[]> ans) {
        if (out.size() != ans.size()){
            return false;
        }
        for(int i=0; i<out.size(); ++i){
            if(ans.get(i).length != out.get(i).length)
                return false;
        }

        Collections.sort(out, new Comparator<int[]>() {
            @Override
            public int compare(int[] s1,int[] s2) {
                for(int i=0 ; i<s1.length ; ++i)
                    if (s1[i] != s2[i])
                        return s1[i]<s2[i] ? -1 : 1;
                return 0;
            }
        });

        for(int i=0; i<out.size(); ++i){
            if(!Arrays.equals(out.get(i), ans.get(i))){
                return false;
            }
        }
        return true;
    }

    static List<int[]> run(Sample s) {
        return new four_sum_sol().fourSum(s.nums, s.target);
    }

    public static void main(String []args) {
        Gson gson = new Gson();
        try {
            Case[] cases = gson.fromJson(new FileReader("four_sum.json"), Case[].class);
            for(int i=0; i<cases.length; ++i) {
                Case c = cases[i];
                long times = 0;
                System.out.println("Score: " + String.valueOf(c.score));
                System.out.println("Case: " + String.valueOf(c.case_name));
                for(int j=0; j<c.data.length; ++j) {
                    Sample s = c.data[j];
                    long clk_s = System.currentTimeMillis();
                    List<int[]> out = run(s);

                    clk_s = System.currentTimeMillis() - clk_s;
                    times += clk_s;

                    if (!compare(out, s.answer)) {
                        for (int[] qwer:out){
                            System.out.print("< " + Arrays.toString(qwer));
                        }
                        for (int[] rewq:s.answer){
                            System.out.print("> " + Arrays.toString(rewq));
                        }
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
        List<int[]> answer;
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
