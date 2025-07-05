from string import Template
my = Template("Today is $today and tomorrow is $tommorow")
out = my.substitute(today ="Monday" , tommorow = "yyy")
print (out)