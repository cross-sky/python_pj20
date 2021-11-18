import pytest

from ef_c5_func import *


ALIVE = '*'
EMPTY = '-'

def test_36_serialize():
    #fial to test this command
    #py_cmd("java -version")
    py_cmd("echo hello")
    

def test_count_neighbors():
    it = count_neighbors(10, 5)
    q1 = next(it)
    q2 = it.send(ALIVE)
    q3 = it.send(ALIVE)
    q4 = it.send(EMPTY)
    q5 = it.send(EMPTY)
    q6 = it.send(EMPTY)
    q7 = it.send(EMPTY)
    q8 = it.send(EMPTY)

    try:
        count = it.send(EMPTY)
    except StopIteration as e:
        print('count: ', e.value)
    
    print(q1, q2, q3, q4, q5, q6, q7)

def test_step_cell():
    it = step_cell(10, 5)
    q0 = next(it)
    ns = [ALIVE, EMPTY, ALIVE, EMPTY, ALIVE, EMPTY, ALIVE, EMPTY]
    qs = [it.send(x) for x in ns]
    
    t1 = it.send(ALIVE)
    print(q0, qs, t1)
    
def test_assign_grid():
    grid = Grid(5, 9)
    grid.assign(0, 3, ALIVE)
    grid.assign(1, 4, ALIVE)
    print(grid)

