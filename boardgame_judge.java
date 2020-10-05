import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonArray;
import com.google.gson.GsonBuilder;

import java.io.FileReader;
import java.io.IOException;

import java.util.ArrayList;
import java.util.List;
/*
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. boardgame_judge.java boardgame_sol.java Judger.java
dk openjdk:14-slim java -cp gson.jar:algs4.jar:. boardgame_judge
*/

public class boardgame_judge extends Judger<List<Boolean>> {

    static class Operation {
        boolean answer;
        JsonArray args;
        String func;
        public Operation() {};
    }

    @Override protected boolean compare(List<Boolean> out, JsonElement s) {
        Gson gson = new Gson();
        Operation[] ops = gson.fromJson(s, Operation[].class);
        int cur = 0;
        for(int i=1; i<ops.length; ++i) {
            switch(ops[i].func){
                case "surrounded":
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
        List<Boolean> output = new ArrayList<Boolean>();
        Gson gson = new Gson();
        Operation[] ops = gson.fromJson(s, Operation[].class);
        boardgame_sol g = new boardgame_sol(ops[0].args.get(0).getAsInt(),
                                            ops[0].args.get(1).getAsInt());
        int[] x, y;
        int ox, oy;
        for (int i=1; i<ops.length; i++) {
            switch(ops[i].func) {
                case "putStone":
                    x = gson.fromJson(ops[i].args.get(0), int[].class);
                    y = gson.fromJson(ops[i].args.get(1), int[].class);
                    g.putStone(x, y, ops[i].args.get(2).getAsCharacter());
                    break;
                case "surrounded":
                    output.add(g.surrounded(ops[i].args.get(0).getAsInt(),
                                            ops[i].args.get(1).getAsInt()));
                    break;
            }
        }
        return output;
    }

    @Override protected void debugPrint(List<Boolean> out, JsonElement s) {
        System.out.print("<");
        for(Boolean b: out) {
            System.out.print(b);
            System.out.print(" ");
        }

        System.out.println("");
        System.out.println(">" + s.toString());
        // Gson gson = new GsonBuilder().setPrettyPrinting().create();
        // System.out.println(">" + gson.toJson(s));
    };

    public static void main(String []args) {
        boardgame_judge j = new boardgame_judge();
        j.judge("boardgame.json");
    }
}
