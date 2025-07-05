def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we're the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")


greet_bob(say_hello)

def parent(num):
    def first_child():
        return "Hi, I'm Elias"

    def second_child():
        return "Call me Ester"

    if num == 1:
        return first_child
    else:
        return second_child