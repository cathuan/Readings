# Porting Python 2 Code to Python 3

This guide is meant to help you figure out how best support both Python 2 & 3 simultaneously.

# The Short Explanation

To make your project be single-source Python 2/3 compatible, the basic steps:
1. Only worry about supporting Python 2.7
2. Make sure you have good test coverage (coverage.y can help)
3. Learn the difference between python 2 and 3
4. Use `Futurize` (or `Modernize`) to update your code
5. Use Pylint to help make sure you don't regress on your Python 3 support
6. Use `caniusepython3` to find out which of your dependencies are blocking your use of Python 3
7. Once your dependencies are no longer blockingg you, use continuous integraton to make sure you stay compatible with Python 2 and 3 (`tox` can help test against multiple versions of Python)
8. Consider using optional static checking to make sure your type usage works in both Python 2 & 3 (e.g. use `mypy` to check your typing under both Python 2 & Python 3)


## Use Python -Qwarm program.py  or -Qwarmall to warm the divisions. It will be very helpful.
Check pep238
https://www.python.org/dev/peps/pep-0238/


# Details

A key point about supporting Python 2 & 3 simultaneously is that you can start **today**! 
- Even if your dependencies are not supposrting Python 3 yet that does not mean you can't modernize your code **now** to support Python 3.
- Most changes required to support Python 3 lead to cleaner code using newer practices even in Python 2 code.
- Anothher key point is that modernizing your Python 2 code to also support Python 3 is largely automated for you.
- The low level work is not mostly done for you and thus can at least benefit from the automated changes immediately.

## Drop support for Python 2.6 and older


## Make sure you specify the proper version support in your setup.py file.

## Have good test coverage

Oce you have your code supporting the oldest version of Pythhon 2, you will want to make sure your test suite has good coverage. 

A good rule of thumb is that if you want to be confident enough in your test suite that any failures that appear after having tools rewrite your code are actually bugs in thhe tools and not in your code.

Try to get 80% coverage rate, and maybe get 90% coverage. `coverage.py` is a good way to do so.

## Learn the differences betwee Python 2 & 3

Once you have your code well-tested you are ready to begin porting your code to Python 3. But to fully understand how your code is going to change and what you want to look out for while you code, you will want to learn what changes Python 3 makes in terms of Python 2.

What's new in Python: https://docs.python.org/3/whatsnew/index.html
Supporting Python 3: An in-depth guide: http://python3porting.com
Cheat sheet: http://python-future.org/compatible_idioms.html
