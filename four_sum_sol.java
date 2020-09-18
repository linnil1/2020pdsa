import java.util.Arrays;
import java.util.List;
import java.util.HashMap;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Map;
import java.util.Collections;


public class four_sum_sol {
    public static List<int[]> fourSum(int[] nums, int target) {
        List<int[]> ans = new LinkedList<>();
        int len = nums.length;
        Arrays.sort(nums);

        Map<Integer, List<int[]>> two_sum_table = new HashMap<>();
        for (int num_1 = 0; num_1 < len - 1; num_1++) {
            for (int num_2 = num_1 + 1; num_2 < len; num_2++) {
                two_sum_table.computeIfAbsent(nums[num_1] + nums[num_2], k -> new LinkedList<int[]>()).add(new int[]{nums[num_1], nums[num_2]});
            }
        }

        for (int num_1 = 0; num_1 < len - 1; ++num_1) {
            for (int num_2 = num_1 + 1; num_2 < len; ++num_2) {
                int reverse = target - nums[num_1] - nums[num_2];

                if (two_sum_table.containsKey(reverse)) {
                    for (int[] set_1_2 : two_sum_table.get(reverse)) {
                        // System.out.print(set_1_2+"\t");
                        // System.out.println(nums[num_2]);

                        if (set_1_2[0] > nums[num_2]) {
                            int[] hit = new int[]{nums[num_1], nums[num_2], set_1_2[0], set_1_2[1]};
                            Arrays.sort(hit);
                            ans.add(hit);
                        }
                    }
                }
            }
        }

        return ans;
    }
}
