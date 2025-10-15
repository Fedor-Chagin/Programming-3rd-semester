def task_1(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return [] 

if __name__ == "__main__":
    nums = list(map(int, input().split())) 
    target = int(input())
    
    result = task_1(nums, target) 
    
    if result:
        print(result[0], result[1])
    else:
        print("Решение не найдено")