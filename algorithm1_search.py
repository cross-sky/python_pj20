""" order algorithms
https://www.runoob.com/w3cnote/ten-sorting-algorithm.html
  """

def find_smallest(arr):
    s = arr[0]
    index = 0
    for i in range(1, len(arr)):
        if s > arr[i]:
            s = arr[i]
            index = i
    return index

def selection_sort_book(arr: list):
    result_arr = []
    for i in range(len(arr)):
        small_index = find_smallest(arr)
        result_arr.append(arr[small_index])
        arr.pop(small_index)
    return result_arr

def bubble_swap(arr: list):
    pass

# my , looks like i misunderstand it. it is actually the selection sort
def bubble_sort(arr: list):
    for i in range(len(arr) - 1):
        # small = arr[i]
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                arr[j], arr[i] = arr[i], arr[j]
    return arr

def bubble_sort_1(arr: list):
    for i in range(1, len(arr)):
        for j in range(len(arr) - i):
            if arr[j] > arr[j+1]:
                arr[j+1], arr[j] = arr[j], arr[j+1]
    return arr

def selection_sort(arr: list):
    for i in range(len(arr) - 1):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = i
        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]
    
def insertion_sort(arr: list):
    for i in range(len(arr)-1):
        sort_index = i
        x = arr[i + 1]
        for j in range(sort_index, -1, -1):
            if x < arr[j]:
                arr[j + 1] = arr[j]
            else:
                arr[j + 1] = x
                break
            if j == 0:
                arr[j] = x
    return arr

def insertion_sort_s(arr: list):
    for i in range(len(arr)):
        pre_index = i - 1
        cur_index = i
        while pre_index >= 0 and arr[pre_index] > arr[cur_index]:
            arr[pre_index + 1] = arr[pre_index]  
            pre_index -= 1
        arr[pre_index + 1] = arr[cur_index]
    return arr


def shell_sort(arr: list):
    n = len(arr)
    step_n = []
    while n > 1:
        n = n//2
        step_n.append(n)
    for s in step_n:
        i = 0
        while i + s < len(arr):
            if arr[i] > arr[i + s]:
                arr[i], arr[i + s] = arr[i + s], arr[i]
            i += 1
    arr = insertion_sort(arr)
    return arr

def shell_sort_1(arr: list):
    # for d in range(len(arr) // 2, 0, )
    n = len(arr)
    step_n = []
    while n > 1:
        n = n // 2
        step_n.append(n)
    
    for d in step_n:
        for i in range(d, len(arr)):
            j = i - d
            while j >= 0:
                if arr[j] > arr[j + d]:
                    arr[j], arr[j + d] = arr[j + d], arr[j]
                j -= d
            print(*arr)
            

    return arr
