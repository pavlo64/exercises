arr = [1,2,3,4]

def sum(arr):
    if len(arr) == 1:
        return arr[0]
    else:
        return arr.pop() + sum(arr)
    
print (sum(arr))