import com.google.gson.JsonElement;

import java.util.Arrays;
import java.util.List;
import java.util.Comparator;
import java.util.Collections;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. three_sum.judge.java three_sum.sol.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<List<int[]>> {

    static class Sample {
        int[] nums;
        List<int[]> answer;
        public Sample() {}
    }

    @Override protected boolean compare(List<int[]> out, JsonElement ele) {
        List<int[]> ans = this.gson.fromJson(ele, Sample.class).answer;

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

    @Override protected List<int[]> run(JsonElement ele) {
        Sample s = this.gson.fromJson(ele, Sample.class);
        return new Solution().threeSum(s.nums);
    }

    @Override protected void debugPrint(List<int[]> out, JsonElement ele) {
        Sample s = this.gson.fromJson(ele, Sample.class);

        for (int[] i:out){
            System.out.print("< " + Arrays.toString(i) + "\n");
        }
        for (int[] i:s.answer){
            System.out.print("> " + Arrays.toString(i) + "\n");
        }
    };

    public static void main(String []args) {
        Judge j = new Judge();
        j.judge("three_sum.json");
    }
}
