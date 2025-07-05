from string import Template as T1 
from jinja2 import Template as T2
info = {'girl1': 'Mary', 'girl2': 'Samantha', 'girl3': 'girl2', 'girl4': 'girl1',

'city1': 'Moscow', 'city2': 'city1'}
t1 = T1("{{$girl4}} and {{$girl3}} arrived at the {{$city2}} station early and waited for the bus.")
print (t1)
out1 = t1. substitute (info)
print (out1)
out2 = T2(out1)
print (out2)
print (out2.render(info))