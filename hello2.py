import time

import hello
def func2():
    f = open("text.txt", "a")
    f.write("hello\n")
    f.close()
    print("Function 2 is active")

if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    func2()
    hello.func1()