import com.google.gson.Gson;
import com.google.gson.JsonElement;

import java.io.FileReader;
import java.io.IOException;

import java.util.ArrayList;
import java.util.List;
/*
dk openjdk:8-slim javac -cp gson.jar:algs4.jar:. percolation_judge.java percolation_sol.java Judger.java
dk openjdk:8-slim java -cp gson.jar:algs4.jar:. percolation_judge
*/

public class percolation_judge extends Judger<List<Boolean>> {

    static class Operation {
        boolean answer;
        int[] args;
        String func;
        public Operation() {};
    }

    @Override protected boolean compare(List<Boolean> out, JsonElement s) {
        Gson gson = new Gson();
        Operation[] ops = gson.fromJson(s, Operation[].class);

        for(int i=1, cur=0; i<ops.length; ++i) {
            switch(ops[i].func){
                case "isOpen":
                case "isFull":
                    if (ops[i].answer != out.get(cur)){
                        return false;
                    }
                    cur++;
                    break;
            }
        }
        return true;
    }

    @Override protected List<Boolean> run(JsonElement s) {
        Gson gson = new Gson();
        Operation[] ops = gson.fromJson(s, Operation[].class);
        List<Boolean> output = new ArrayList<Boolean>();

        percolation_sol sol = new percolation_sol(ops[0].args[0]);
        for (int i=1 ; i<ops.length ; i++){
            switch(ops[i].func){
                case "open":
                    sol.open(ops[i].args[0],
                             ops[i].args[1]);
                    break;
                case "isOpen":
                    output.add(Boolean.valueOf(sol.isOpen(ops[i].args[0],
                                                          ops[i].args[1])));
                    break;
                case "isFull":
                    output.add(Boolean.valueOf(sol.isFull(ops[i].args[0],
                                                          ops[i].args[1])));
                    break;
                case "percolates":
                    output.add(Boolean.valueOf(sol.percolates()));
                    break;
            }
        }
        return output;
    }

    @Override protected void debugPrint(List<Boolean> out, JsonElement s) {} ; 

    public static void main(String []args) {
        percolation_judge j = new percolation_judge();
        j.judge("percolation.json");
    }
}
