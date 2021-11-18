import pytest

from ef_c2_func import *


def test_sort_priority():
    numbers = [8, 3, 1, 2, 5, 4, 7, 6]
    group = {2, 3, 5, 7}
    sort_result = sort_priority(numbers, group)
    print(sort_result)