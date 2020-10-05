import java.util.List;
import java.util.Arrays;
import java.util.LinkedList;


class Solution {
    public List<int[]> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<int[]> ans = new LinkedList<>(); 

        for (int i = 0; i < nums.length-2; i++) {
            int left = i + 1;
            int right = nums.length - 1;
            int target = 0 - nums[i];

            while (left < right) {
                if (nums[left] + nums[right] == target) {
                    ans.add(new int[]{nums[i], nums[left], nums[right]});
                    
                    left++; 
                    right--;
                } 
                else if (nums[left] + nums[right] < target) ++left;
                else --right;
           }
            
        }
        return ans;
    }
}
