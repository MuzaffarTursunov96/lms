nums =[1,2,3]


    
class Solution(object):
    def permute(self, nums):
        result = []
        n = len(nums)
        counter = 0
        
        while counter <= n:
            
            for i in range(counter+1, n):
                new_nums = nums.copy()
                new_nums[counter], new_nums[i] = new_nums[i], new_nums[counter]
                print(nums)
                result.append(new_nums)
            counter += 1
        
        return result
    
a = Solution()
print(a.permute(nums))


