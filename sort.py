import time
arr = [5, 3, 6, 2, 10]
start_time = time.time()
def findSmallest(arr):
    smallest = arr[0]
    smallest_index = 0 
    for i in range(1, len(arr)): 
        if arr[i] < smallest: 
            smallest = arr[i] 
            smallest_index = i 
    return smallest_index


def selectionSort(arr): 
    newArr = [] 
    for i in range(len(arr)): 
        smallest = findSmallest(arr)
        newArr.append(arr.pop(smallest)) 
    return newArr 

end_time = time.time()
execution_time = end_time - start_time
print (selectionSort(arr))
print(execution_time)