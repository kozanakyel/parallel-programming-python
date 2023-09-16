

def merge(A: list, B: list) -> list:
    i = 0 
    j = 0
    k = 0
    m = len(A)
    n = len(B)
    
    merged = [None]*(m+n)
    
    while i < m and j < n:
        if A[i] <= B[j]:
            merged[k] = A[i]
            i += 1
        else:
            merged[k] = B[j]
            j += 1
        k += 1
        
    while i < m:
        merged[k] = A[i]
        i += 1
        k += 1

    while j < n:
        merged[k] = B[j]
        j += 1
        k += 1           
    
    return merged

def find_median(arr: list):
    l = len(arr)
    if l % 2 == 1:
        return arr[l // 2]
    else:
        mid1 = arr[(l // 2) - 1]
        mid2 = arr[l // 2]
        return (mid1 + mid2) / 2

if __name__ == '__main__':
    input1 = input("input1: ").split()
    input2 = input("input2: ").split()
    
    input1 = [float(num) if '.' in num else int(num) for num in input1]
    input2 = [float(num) if '.' in num else int(num) for num in input2]
    
    concated_arr = merge(input1, input2)
    median_result = find_median(concated_arr)
    print(f"output: {median_result}")
    
    