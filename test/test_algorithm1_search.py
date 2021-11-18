import pytest
from algorithm1_search import *


def test_bubble_sort_1():
    arr = [3, 9, 7, 5, 4]
    sort_arr = bubble_sort_1(arr)
    print(*sort_arr)

def test_bubble_sort():
    arr = [3, 9, 7, 5, 4]
    sort_arr = bubble_sort(arr)
    print(*sort_arr)


def test_insertion_sort():
    arr = [3, 9, 7, 5, 4]
    sort_arr = insertion_sort(arr)
    print(*sort_arr)

def test_shell_sort():
    arr = [7, 6, 5, 4, 3, 2, 1]
    sort_arr = shell_sort(arr)
    print(*sort_arr)

    
def test_shell_sort_1():
    arr = [8, 7, 6, 5, 4, 3, 2, 1]
    sort_arr = shell_sort_1(arr)
    print(*sort_arr)