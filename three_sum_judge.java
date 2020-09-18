import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;

import java.io.FileReader;
import java.io.IOException;

import java.util.Arrays; 
import java.util.List;
import java.util.Collections;
import java.util.*;

/*
dk openjdk:8-slim javac -cp gson.jar two_sum_judge.java  two_sum_sol.java
dk openjdk:8-slim java -cp gson.jar:. two_sum_judge
*/

public class three_sum_judge {
    static boolean compare(List<int[]> out, List<int[]> ans) {
        if (out.size()!=ans.size()){
            return false;
        }

        Collections.sort(ans,new Comparator<int[]>() {
            @Override
            public int compare(int[] s1,int[] s2) {
                int size,comp;
                if (s1.length>s2.length){
                    size = s2.length;
                }
                else{
                    size=s1.length;
                }
                for(int i = 0;i<size;++i){
                    comp=s1[0]-s2[0];
                    if(comp!=0){
                        return (comp>0?1:-1);
                    }
                }
                return 0;
            }
        });
        for(int i = 0; i < out.size(); ++i){
            if(!Arrays.equals(out.get(i),ans.get(i))){
                return false;
            }
        }
        return true;
    }

    static List<int[]> run(Sample s) {
        return new three_sum_sol().threeSum(s.nums);
    }

    public static void main(String []args) {
        Gson gson = new Gson();
        try {
            Case[] cases = gson.fromJson(new FileReader("three_sum.json"), Case[].class);
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
                            System.out.print("< " + qwer.toString());                            
                        }
                        for (int[] rewq:s.answer){
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
