import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. restaurants.judge.java restaurants.sol.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. Judge
*/

class Judge extends Judger<List<int[]>> {

    static class Operation {
        JsonElement answer;
        JsonArray args;
        String func;
        public Operation() {};
    }

    @Override protected boolean compare(List<int[]> out, JsonElement s) {
        Operation[] ops = this.gson.fromJson(s, Operation[].class);
        int cur = 0;
        for(int i=1; i<ops.length; ++i) {
            switch(ops[i].func){
                case "filter":
                    if (!Arrays.equals(this.gson.fromJson(ops[i].answer, int[].class),
                                       out.get(cur)))
                        return false;
                    cur++;
                    break;
            }
        }
        return true;
    }

    @Override protected List<int[]> run(JsonElement s) {
        Operation[] ops = this.gson.fromJson(s, Operation[].class);
        List<int[]>[] restaurants = this.gson.fromJson(ops[0].args, new TypeToken<List<int[]>[]>(){}.getType());
        List<int[]> output = new ArrayList<int[]>();

        this.resetTime();
        Restaurants sol = new Restaurants(restaurants[0]);
        this.updateTime();
        for (int i=1; i<ops.length; i++) {
            switch(ops[i].func) {
                case "filter":
                    this.resetTime();
                    output.add(
                        sol.filter(ops[i].args.get(0).getAsInt(),
                                   ops[i].args.get(1).getAsInt())
                    );
                    this.updateTime();
                    break;
            }
        }
        this.resetTime();
        return output;
    }

    @Override protected void debugPrint(List<int[]> out, JsonElement s) {
        /*
        for (int[] a: out)
            System.out.println("<" + Arrays.toString(a));
        System.out.println(">" + gson.toJson(s));
        */
    };

    public static void main(String []args) {
        Judge j = new Judge();
        j.judge("restaurants.json");
    }
}
