DEBUG = 1

def my_print(str, debug=1):
    if debug:
        print(str)


class MyPrint:
    def __init__(self, debug=1):
        self.debug =debug
    
    def my_print(self, strs):
        if self.debug:
            print(strs)

 