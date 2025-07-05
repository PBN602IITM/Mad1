def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

def decorator_factory(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            funny_stuff()
            something_with_argument(argument)
            result = function(*args, **kwargs)
            more_funny_stuff()
            return result
        return wrapper
    return decorator

@decorator_factory("Some argument")
def function_to_be_decorated(args):
    print(f"Do something with '{args}'.")

created_decorator = decorator_factory("Some argument")

@created_decorator
def function_to_be_decorated(args):
    print(f"Do something with '{args}'.")

def funny_stuff():
    print("This is some funny stuff happening before the function call.")   

def something_with_argument(argument):
    print(f"Doing something with the argument: {argument}") 

def more_funny_stuff():
    print("This is some more funny stuff happening after the function call.")   

def do_twice_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper

def decorator_with_args(arg1, arg2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Decorator arguments: {arg1}, {arg2}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
def decorator_with_args_factory(arg1, arg2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Decorator arguments: {arg1}, {arg2}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
def decorator_with_args_and_kwargs(arg1, arg2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Decorator arguments: {arg1}, {arg2}")
            return func(*args, **kwargs)
        return wrapper
    return decorator    
def decorator_with_args_and_kwargs_factory(arg1, arg2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"Decorator arguments: {arg1}, {arg2}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

