
from os import close
import time
import subprocess
from queue import Empty, Queue
from threading import Thread
from collections import namedtuple

def py_cmd(command):
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8')
    # subp.wait(2)
    while True:
        flag = 1
        if subp.poll() != 0:
            flag = 0
        if flag:
            break
        else:
            print('task is still running')
            time.sleep(1)
    if subp.poll() == 0:
        out, err = subp.communicate()
        print(out)
        print(err)
    else:
        print('Fail')


class ClosableQueue(Queue):
    SENTINEL =  object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue) -> None:
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
    
    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

    
# life game
"""
1. get neighbors states count
2. judge cur state
"""

ALIVE = '*'
EMPTY = '-'

Query = namedtuple('Query', ('y', 'x'))
Transition =  namedtuple('Transition', ('y', 'x', 'state'))
def count_neighbors(y, x):
    n_ =  yield Query(y+1, x+0)
    ne = yield Query(y + 1, x + 1)
    e_ = yield Query(y, x + 1)
    se = yield Query(y - 1, x + 1)
    s_ = yield Query(y - 1, x)
    sw = yield Query(y - 1, x - 1)
    w_ = yield Query(y, x - 1)
    nw = yield Query(y + 1, x - 1)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state

def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)

TICK = object()

def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK

class Grid():
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self) -> str:
        result = '\n'
        for y in range(self.height):
            for x in range(self.width):
                result += self.rows[y][x]
            result += '\n'
        return result
    
    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

def live_a_generation(grid: Grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny




