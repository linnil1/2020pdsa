// Code provided by B05611003
import java.util.Arrays; 
import java.util.TreeMap; 


class Solution {
    static int[] twoSum(int[] nums, int target) {
        TreeMap<Integer, Integer> map = new TreeMap<Integer, Integer>();
        for (int i=0; i<nums.length; ++i) {
            int now = nums[i];
            try {
                return new int[]{map.get(target - now), i};
            } catch (java.lang.NullPointerException e) {
                map.put(now, i);
            }
        };
        return new int[]{0, 0};
    }

    // remove main before submit 
    public static void main(String []args) {
        System.out.println(Arrays.toString(twoSum(new int[]{2,7,11,15}, 26)));
    }
}
