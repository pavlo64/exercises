def binary_search(list, item):
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = int(low + high)//2
        guess = list[mid]
        if guess == int(item):
            return mid
        if guess > int(item):
            high = mid -1
        else:
            low = mid +1
    return None
if __name__ == '__main__':
    my_list = [1, 3, 5, 6, 7, 89, 9, 45, 346, 45, 64, 87, 4, 7468, 35, 457, 786, 0, 967, 7654, 45]

    my_list = sorted(my_list)
    item = 35

    print (binary_search(my_list, item))
    print (my_list)