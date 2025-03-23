def quicksort(array): 
    if len(array) < 2: 
        return array 
    else: 
        pivot = array[0] 
        less = [i for i in array[1:] if i<= pivot] 
        greater = [ i for i in array[ 1: ] if i > pivot]
    return quicksort(less) + [pivot] + quicksort(greater) 

if __name__ == '__main__':
    arr = [5,7,8,9,3,2,1]
    print (quicksort(arr))