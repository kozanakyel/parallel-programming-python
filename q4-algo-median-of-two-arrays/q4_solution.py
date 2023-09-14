from typing import List

def merge(A: List, B: List) -> []:
    i = 0 
    j = 0
    k = 0
    m = len(A)
    n = len(B)
    
    result = [None]*(m+n)
    
    while i < m and j < n:
        if A[i] <= B[j]:
            result[k] = A[i]
            i += 1
        else:
            result[k] = B[j]
            j += 1
        k += 1
        
    if i < m:
        for p in range(i, m):
            result[k] = A[p]
            k += 1
    else:
        for p in range(j, n):
            result[k] = B[p]
            k += 1            
    
    return result

def find_median(arr: List):
    total_length = len(arr)
    if total_length % 2 == 1:
        return arr[total_length // 2]
    else:
        mid1 = arr[(total_length // 2) - 1]
        mid2 = arr[total_length // 2]
        return (mid1 + mid2) / 2

if __name__ == '__main__':
    input1 = input("input1: ").split()
    input2 = input("input2: ").split()
    
    input1 = [float(num) if '.' in num else int(num) for num in input1]
    input2 = [float(num) if '.' in num else int(num) for num in input2]
    
    concated_arr = merge(input1, input2)
    median_result = find_median(concated_arr)
    print(f"median: {median_result}")
    
    