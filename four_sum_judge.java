import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.IOException;

import java.util.Arrays; 
import java.util.List;
/*
dk openjdk:8-slim javac -cp gson.jar two_sum_judge.java  two_sum_sol.java
dk openjdk:8-slim java -cp gson.jar:. two_sum_judge
*/

public class four_sum_judge {
    static boolean compare(List<List<Integer>> out, List<List<Integer>> ans) {
        if (out.size()!=ans.size()){
            return false;
        }
        for(int i = 0; i < out.size(); ++i){
            if(!out.get(i).equals(ans.get(i))){
                return false;
            }
        }
        return true;
    }

    static List<List<Integer>> run(Sample s) {
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
                    List<List<Integer>> out = run(s);

                    clk_s = System.currentTimeMillis() - clk_s;
                    times += clk_s;

                    if (!compare(out, s.answer)) { 
                        for (List<Integer> qwer:out){
                            System.out.print("< " + qwer.toString());                            
                        }
                        for (List<Integer> rewq:s.answer){
                            System.out.print("> " + rewq.toString());
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
        List<List<Integer>> answer;
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
