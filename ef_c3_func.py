import collections
from collections import defaultdict
import os
import threading
from typing import Dict, List
import json
# 定义一个namedtuple类型Grade， contain score，weight fields.
Grade = collections.namedtuple('Grade', ('score', 'weight'))

class Subject():
    def __init__(self) -> None:
        self._grades = []

    def report_grades(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score  * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student():
    def __init__(self) -> None:
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

def increment_with_report(current, increments):
    class BetterCountMissing():
        def __init__(self) -> None:
            self.added = 0
        
        def __call__(self, *args: Any, **kwds: Any) -> Any:
            self.added += 1
            return 0
    
    counter = BetterCountMissing()
    result = defaultdict(counter, current)
    for key, amount in increments:
        result[key] += amount
    return result, counter.added

class InputData():
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()
    
class Worker():
    def __init__(self, input_data: InputData) -> None:
        self.input_data = input_data   # InputData
        self.result = None
    
    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()  # read all content
        self.result = data.count('\n')

    def reduce(self, other: Worker):
        self.result += other.result

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

def execute(workers: List(Worker)):
    threads = [threading.Thread(target=w.map) for w  in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)

    return first.result

def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

class GenericInputData():
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

class PathInputDataGeneric(GenericInputData):
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWork():
    def __init__(self, input_data: InputData) -> None:
        self.input_data = input_data   # InputData
        self.result = None
    
    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class: GenericInputData, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCountWorkerGeneric(GenericWork):
    def map(self):
        data = self.input_data.read()  # read all content
        self.result = data.count('\n')

    def reduce(self, other: GenericWork):
        self.result += other.result


def mapreduce_generic(worker_class: GenericWork, inpu_class: GenericInputData, config):
    workers = GenericWork.create_workers(config)
    return execute(workers)


class ToDicMixin():
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict: dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDicMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

class JsonMixin():
    @classmethod
    def from_json(cls, data):
        kwards = json.loads(data)
        return cls(**kwards)

    def to_json(self):
        return json.dumps(self.to_dict())


from collections.abc import Sequence

class BinaryNode():
    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right

class IndexableNode(BinaryNode):
    def _search(self, count, index):
        pass

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index out of range')

        return found.value

class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count

class  BetterNode(SequenceNode, Sequence):
    pass



        