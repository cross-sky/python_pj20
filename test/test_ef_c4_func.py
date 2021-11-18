import pytest

from ef_c4_func import *


def test_35_serialize():
    point = EvenBetterPoint2D(5, 3)
    print('Before:   ', point)
    data = point.serialize()
    print('Serialized: ', data)
    after = deserizlize(data)
    print('After:   ', after)
