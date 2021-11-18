import datetime


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

def sort_priority(values: list, group):
    def helper(x):
        if x in group:
            return (0,x)
        return (1, x)
    return sorted(values, key=helper)
    #values.sort(key=helper)

class Sorter():
    def __init__(self, group) -> None:
        self.group = group
        self.found = False
    
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return(0, x)
        return (1, x)

def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


class ReadVisits():
    def __init__(self, data_path) -> None:
        self.data_path = data_path
    
    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)
            
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100* value / total
        result.append(percent)
    return result

def log(message, *value):
    if not value:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in value)
        print('{}: {}'.format(message, values_str))

def logt(message, when=None):
    """Log a message with a timestamp.

    Args:
        Message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    when = datetime.datetime.now() if when is None else when
    print("{}: {}".format(when, message))

    