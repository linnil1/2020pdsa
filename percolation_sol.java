// author: linnil1
// DFS for open query
import java.lang.Math;
import java.util.Stack;

public class percolation_sol {

    private boolean[][] board;
    private int[][] id;
    private int[][] is_travel;
    private int N, len;
    private boolean percolated;

    percolation_sol(int n) {
        // init all things
        N = n;
        percolated = false;
        board = new boolean[N][N];
        id = new int[N][N];
        is_travel = new int[N][N];
        for (int i=0 ; i<N; ++i)
            for (int j=0 ; j<N; ++j) {
                board[i][j] = false;
                id[i][j] = i * N + j;
                is_travel[i][j] = -1;
            }
    }

    private boolean isTop(int i) {
        // is id in the top row
        return i < N;
    }

    private int toID(int x, int y) {
        // (x, y) to id
        return x * N + y;
    }

    public void open(int row, int col) {
        // open site (row, col) if it is not open already
        board[row][col] = true;
        Stack<int[]> stack = new Stack<int[]>(); 
        Stack<int[]> all = new Stack<int[]>(); 

        // put first one into stack
        stack.push(new int[]{row, col});
        int now_id = id[row][col];
        int now_max = now_id;
        int now_min = now_id;

        // triversal
        while(!stack.empty()){
            int[] tmp = stack.pop();
            all.push(tmp);
            int[] dir = new int[]{0, -1,
                                 -1,  0,
                                  1,  0,
                                  0,  1};
            // Tree pruning
            if (!(row == tmp[0] && col == tmp[1]) && isTop(id[tmp[0]][tmp[1]]))
                continue;

            // to up down left right
            for(int i=0; i<8; i+=2) {
                int x = tmp[0] + dir[i],
                    y = tmp[1] + dir[i+1];
                if (x >= 0 && y >= 0 && x < N && y < N && 
                        board[x][y] && is_travel[x][y] != now_id) {
                    now_min = Math.min(now_min, id[x][y]);
                    now_max = Math.max(now_max, toID(x, y));
                    is_travel[x][y] = now_id;
                    stack.push(new int[]{x, y});
                }
            }
        }

        // update only when connected to top
        if(isTop(now_min)) {
            // is percolates ?
            if (now_max >= toID(N - 1, 0))
                percolated = true;
            // assign min
            while(!all.empty()){
                int[] tmp = all.pop();
                id[tmp[0]][tmp[1]] = now_min;
            }
        }
    }

    public boolean isOpen(int row, int col) {
        // is site (row, col) open?
        return board[row][col];
    }

    public boolean isFull(int row, int col) {
        // is site (row, col) full?
        return isTop(id[row][col]);
    }

    public boolean percolates() {
        // does the system percolate?
        return percolated;
    }

    public static void main(String[] args) {
        // test
        percolation_sol s = new percolation_sol(3);
        s.open(1,1);
        System.out.println(s.isFull(1, 1));
        System.out.println(s.percolates());
        s.open(0,1);
        s.open(2,0);
        System.out.println(s.isFull(1, 1));
        System.out.println(s.isFull(0, 1));
        System.out.println(s.isFull(2, 0));
        System.out.println(s.percolates());
        s.open(2,1);
        System.out.println(s.isFull(1, 1));
        System.out.println(s.isFull(0, 1));
        System.out.println(s.isFull(2, 0));
        System.out.println(s.isFull(2, 1));
        System.out.println(s.percolates());
    }
}

