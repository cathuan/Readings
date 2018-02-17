from __future__ import division
from __future__ import print_function
from builtins import input
from past.utils import old_div


def greet(name):

    print("Hello, {0}!".format(name))


print("What's your name?")
name = input()
greet(name)

print(old_div(2,3))
print(old_div(2.,3))


# Use 2to3 to fix it. It's a binary file run on bash.
