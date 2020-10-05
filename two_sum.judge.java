import com.google.gson.Gson;
import com.google.gson.JsonElement;

import java.util.Arrays;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. two_sum.judge.java two_sum.sol.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<int[]> {

    static class Sample {
        int[] nums;
        int target;
        int[] answer;
        public Sample() {}
    }

    @Override protected boolean compare(int[] out, JsonElement ele) {
        Gson gson = new Gson();
        Sample s = gson.fromJson(ele, Sample.class);
        return Arrays.equals(out, s.answer);
    }

    @Override protected int[] run(JsonElement ele) {
        Gson gson = new Gson();
        Sample s = gson.fromJson(ele, Sample.class);
        return new Solution().twoSum(s.nums, s.target);
    }

    @Override protected void debugPrint(int[] out, JsonElement ele) {
        Gson gson = new Gson();
        Sample s = gson.fromJson(ele, Sample.class);
        System.out.println("< " + Arrays.toString(out));
        System.out.println("> " + Arrays.toString(s.answer));
    };

    public static void main(String []args) {
        Judge j = new Judge();
        j.judge("two_sum.json");
    }
}
