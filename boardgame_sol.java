// author: linnil1
// DFS for open query
import java.lang.Math;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.HashMap;

public class boardgame_sol {
    private HashMap<List<Integer>, Integer> map;
    private ArrayList<Character> stones;
    private ArrayList<Integer> is_travel;
    private ArrayList<Boolean> is_surrouned;
    private int travel_id;

    public boardgame_sol(int h, int w) {
        this.map = new HashMap<List<Integer>, Integer>();
        this.stones = new ArrayList<Character>();
        this.is_travel = new ArrayList<Integer>();
        this.is_surrouned = new ArrayList<Boolean>();
        this.travel_id = -1;

        // create a board of size h*w
    }

    public void putStone(int[] x, int[] y, char stoneType) {
        // put stones on the board according to the coordinates
        // init stone
        for(int i=0; i<x.length; ++i) {
            this.map.put(Arrays.asList(x[i], y[i]), this.stones.size());
            this.is_travel.add(-1);
            this.stones.add(stoneType);
            this.is_surrouned.add(false);
        }

        // go triversal
        for(int i=0; i<x.length; ++i) {
            int[] dir = new int[]{0,  0,
                                  0, -1,
                                 -1,  0,
                                  1,  0,
                                  0,  1};
            for(int j=0; j<10; j+=2) {
                int ox = x[i] + dir[j],
                    oy = y[i] + dir[j+1];
                if (this.map.containsKey(Arrays.asList(ox, oy)))
                    triversal(ox, oy);
            }
        }
    }

    private boolean triversal(int x, int y) {
        this.travel_id += 1;
        Stack<List<Integer>> stack = new Stack<List<Integer>>();
        Stack<Integer> all = new Stack<Integer>();
        stack.push(Arrays.asList(x, y));
        int id = this.map.get(stack.peek());
        char stone = this.stones.get(id);
        all.push(id);

        // triversal
        while(!stack.empty()) {
            List<Integer> xy = stack.pop();
            int[] dir = new int[]{0, -1,
                                 -1,  0,
                                  1,  0,
                                  0,  1};
            for(int i=0; i<8; i+=2) {
                List<Integer> newxy = Arrays.asList(xy.get(0) + dir[i], xy.get(1) + dir[i+1]);
                if (this.map.containsKey(newxy)) {
                    id = this.map.get(newxy);
                    if (this.is_travel.get(id) != this.travel_id && 
                        this.stones.get(id) == stone) {
                        this.is_travel.set(id, this.travel_id);
                        stack.push(newxy);
                        all.push(id);
                    }
                } else {
                    return false;
                }
            }
        }

        // is surrouneded ->
        while(!all.empty()) {
            this.is_surrouned.set(all.pop(), true);
        }
        return true;
    }

    public boolean surrounded(int x, int y) {
        // Answer if the stone and its connected stones are surrounded by another type of stones
        return this.is_surrouned.get(this.map.get(Arrays.asList(x, y)));
    }

    public char getStoneType(int x, int y) {
        return this.stones.get(this.map.get(Arrays.asList(x, y)));
    }

    public static void main(String[] args) {
        // test
        boardgame_sol g = new boardgame_sol(3, 3);
        g.putStone(new int[]{1}, new int[]{1}, 'O');
        System.out.println(g.surrounded(1, 1));

        g.putStone(new int[]{0, 1, 1}, new int[]{1, 0, 2}, 'X');
        System.out.println(g.surrounded(1, 1));

        g.putStone(new int[]{2}, new int[]{1}, 'X');
        System.out.println(g.surrounded(1, 1));
        System.out.println(g.surrounded(2, 1));

        g.putStone(new int[]{2}, new int[]{0}, 'O');
        System.out.println(g.surrounded(2, 0));
    }
}

