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
This one can be caught by `-3` flag as well.

## `Pylint` to give warning for python 3 compatibility

Use `pylint --py3k` flag to lint your code to receive warnings when your code begins to deviate from `Python 3` compatibility.

## Use python's internal warning sign

Use `python -3` flag to be warned bout various compatibility issues.

Use `python -Werror` flag to crash code when you receive a warning, or `python -We::Depreciation` which turns depreciation warnings into error

May check pep230 https://www.python.org/dev/peps/pep-0230/


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


### `print` is a function now

Now the `print` statement is a function. Some advantage is

- Use `print(x, end="")` to decide the end char of a print, instead of previous `print x,`
- Use `print(x, file=f)` to determine the output pipe instead of `print >>f, x`
- Use `print(x, y, z, sep="")` to determine the separation between strings. Previously you have no choice.

Python `2to3` binary can change `print` quickly.

### `Views` and `Iterators` instead of `List`

Some APIs no longer return list

- `dict.keys()`, `dict.items()` and `dict.values()` now return `views` instead of `list`.
- `dict.iterkeys()`, `dict.iteritems()` and `dict.itervalues()` are removed
- `map()` and `filter()` return `iterators`.
- `range()` return an `iterator`, and `xrange()` is removed.
- `zip()` returns an `iterator`.

### Integers

- There is no longer `long`.
- Division
- `sys.maxint` is removed. But `sys.maxsize` gives an integer larger than any practical list or string index.
- `repr` of a long integer does not have `L` in it.
- `Octal` is no longer of the form `0720`. Use `0o720` instead.

## Use tools to convert Py2 code to Py3 compatible

Use `Futurize` or `Moderize`. The later one is more conservative.

This will create a patch. People can apply the patch to the file to create new files.

`Futurize` has two stages. `state1` and `stage2`. Check the document.

# What's our concern?

- Divisions: this should be handled. Use `python -3` or so to crash any division, manually fix all of them. Or I think `futurize` program makes it work pretty well.
- binary data: we have multiple binary stuffs parsing. This may causes a problem. Hopefully futurize will solve it.
- __cmp__ may be a concern?
- How about `cython` code we are regularly using? Some of the code depends on `cython`.
- Start to use `pathlib` instead of `os.path`. Should not be a big problem right?

Can't think anything else
