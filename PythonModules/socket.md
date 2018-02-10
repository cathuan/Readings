# `socket`: Low-level networking interface

This module provides access to the BSE *socket* interface, which is available on all modern Unix systems, Windows, Mac OS X, etc.

Python abstracts system level sockets function calls in C:

The `socket()` function returns a `socket` object whose methods implement the various socket system calls. It is similar to a file handler `open(filename)`. Buffer is automatically and the buffer length is implicit on sending operations.

Socket addresses are represented as:
- A single string is used for the `AF_UNIX` address family.
- A pair `(host, port)` is used for the `AF_INET` address family.
- For `AF_INET6` address family, a 4-tuple `(host, port, flowinfo, scopeid)` is used. For `socket` module methods, `flowinfo` and `scopeid` represents `sin6_flowinfo` and `sin6_scope_id` in original C `struct` can be omitted just for backward compatibility.
- Other address families are currently not supported.

## `socket` constants

There are some socket constants used for different purposes (when initializing the `socket` object).
