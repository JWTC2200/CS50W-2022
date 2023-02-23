def announce(f):
    def w():
        print("ABC")
        f()
        print("XYZ")
    return w

@announce
def hello():
    print("hello")
    
hello()