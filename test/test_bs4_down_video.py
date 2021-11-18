import pytest
from bs4_down_video import *


def test_getHeaders_test():
    testurl = 'https://www.agefans.net/detail/20210036'
    myhead = Myheaders(testurl)
    #domain = myhead.createHost()
    myhead.createHost()
    print(myhead.host)
    assert myhead.host == 'www.agefans.net'