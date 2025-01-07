from collections.abc import Generator


def trampoline(func:Generator):
    stack = (func, ())
    value = None
    while stack:
        coroutine, stack = stack
        try:
            value = coroutine.send(value)
            assert isinstance(value, Generator), "yielding is only used for function calls back to the runtime"
        except StopIteration as e:
            value = e.value
            # functions can return a value or a function call (tail call optimization!)
        if isinstance(value, Generator):
            # if we got a coroutine, add it to the stack
            stack = (value, (coroutine, stack))
            value = None
    return value

def consumer(func):
    def wrapper(*args,**kw):
        gen = func(*args, **kw)
        try:
            next(gen)
        except StopIteration as e:
            return e.value
        return gen
    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__  = func.__doc__
    return wrapper

# @consumer
def dfs(n=4, path=""):
    if n == 0:
        print(path)
        return 1
    s = 0
    s += yield dfs(n-1, path + "L")
    s += yield dfs(n-1, path + "R" )
    return s


def main():
    print(trampoline(dfs()))

if __name__ == '__main__':
    main()