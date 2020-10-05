// The solution is provided by B05611003
import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class percolation_sol {

	private int site_length;
	private boolean[][] sites;
	private WeightedQuickUnionUF UF;
	private WeightedQuickUnionUF full;
	private int top_virtual;
	private int bottom_virtual;
	private int open_site = 0;

	public percolation_sol (int n){		// create n-by-n grid, with all sites blocked
		if (n <= 0) throw new IllegalArgumentException("");
		site_length = n;
		sites = new boolean[n][n];
		UF = new WeightedQuickUnionUF((n*n)+2);
		full = new WeightedQuickUnionUF((n*n)+2);	//N^2sites+top+bottom
		top_virtual = n*n;
		bottom_virtual = n*n+1;
	}              
	public void open(int row, int col){			// open site (row, col) if it is not open already
		//check(row,col);
		open_site++;
		sites[row][col] = true;
		if (row == 0) {
			UF.union(xyTo1D(row,col),top_virtual);
			full.union(xyTo1D(row,col),top_virtual);
		}
		if (row == site_length-1) {
			UF.union(xyTo1D(row,col),bottom_virtual);
		}
		if (row-1 >= 0 && isOpen(row-1,col)) {
			UF.union(xyTo1D(row-1,col),xyTo1D(row,col));
			full.union(xyTo1D(row-1,col),xyTo1D(row,col));

		}//up
		if (row+1 < site_length && isOpen(row+1,col)) {
			UF.union(xyTo1D(row+1,col),xyTo1D(row,col));
			full.union(xyTo1D(row+1,col),xyTo1D(row,col));			
		}//down
		if (col-1 >= 0 && isOpen(row,col-1)) {
			UF.union(xyTo1D(row,col-1),xyTo1D(row,col));
			full.union(xyTo1D(row,col-1),xyTo1D(row,col));
		}//left
		if (col+1 < site_length && isOpen(row,col+1)) {
			UF.union(xyTo1D(row,col+1),xyTo1D(row,col));
			full.union(xyTo1D(row,col+1),xyTo1D(row,col));
		}//right
		// for (int i = 1; i <= site_length; i++){
		// 	if (UF.connected(xyTo1D(site_length,i),top_virtual)){UF.union(xyTo1D(site_length,i),bottom_virtual);}
		// }
		//if (row == site_length && isFull(row,col)) {UF.union(xyTo1D(row,col),bottom_virtual);}
	}   
	public boolean isOpen(int row, int col){	// is site (row, col) open?
		//check(row,col);
		return sites[row][col];
	}
	public boolean isFull(int row, int col){	// is site (row, col) full?
		//check(row,col);
		return full.connected(xyTo1D(row,col),top_virtual);
	} 
	public int numberOfOpenSites(){				// number of open sites
		return open_site;
	}      
	public boolean percolates(){				// does the system percolate?
		return UF.connected(bottom_virtual,top_virtual);
	}         
	private int xyTo1D(int x, int y){
		return (x)*site_length+(y);
	}
	private void check(int i,int j){
		if (i < 0 || i >= site_length) throw new IllegalArgumentException("row index i out of bounds");
		if (j < 0 || j >= site_length) throw new IllegalArgumentException("row index j out of bounds");
	}
	//public static void main(String[] args){};	// test client (optional)
}

