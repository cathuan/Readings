# `socket`: Low-level networking interface

This module provides access to the BSE *socket* interface, which is available on all modern Unix systems, Windows, Mac OS X, etc.

Python abstracts system level sockets function calls in C:

The `socket()` function returns a `socket` object whose methods implement the various socket system calls. It is similar to a file handler `open(filename)`. Buffer is automatically and the buffer length is implicit on sending operations.

Socket addresses are represented as:
- A single string is used for the `AF_UNIX` address family.
- A pair `(host, port)` is used for the `AF_INET` address family.
- For `AF_INET6` address family, a 4-tuple `(host, port, flowinfo, scopeid)` is used. For `socket` module methods, `flowinfo` and `scopeid` represents `sin6_flowinfo` and `sin6_scope_id` in original C `struct` can be omitted just for backward compatibility.
- Other address families are currently not supported.

## `socket` constants and methods

There are some socket constants used for different purposes (when initializing the `socket` object).

### `socket([family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)

Create a new socket.

- The address family should be `AF_INET`, `AF_INET6` or `AF_UNIX`.
- The socket type should be `SOCK_STREAM`, `SOCK_DGRAM` or maybe one of the `SOCK_` constants.
- The protocol number is usually zero and may be omitted.

### `socketpair([family[, type[, proto]]])`

Build a connected socket objects.

### `AF_UNIX`, `AF_INET` and `AF_INET6`

These represents the address (and protocal) families, used for the first argument of `socket()`.

### `SOCK_STREAM`, `SOCK_DGRAM`, `SOCK_RAM`, `RDM` and `SOCK_SEQPACKET`

These represent the socket type, used for the second argument to `socket()`.

### `has_ipv6`

This constants contains a boolean value which indicates if IPv6 is supported on this platform.


### `create_connection(address[, timeout[, source_address]])`

Connect to a TCP service listeningg on the internet address `(host, port)`, and return the `socket` object.

This is a higher level function comparing to `connect()`. If `host` is a non-numeric hostname, it will try to resolve it for both `AF_INET` and `AF_INET6`, and then try to connect to all possible addresses in turn until a connection succeeds.

`timeout` is set the timeout on the socket instance before attempting to connect.

`source_address` is a `(host, port)` tuple for the socket to bind to as its source address before connecting.


### `getaddrinfo(host, port[, family[, sockettype[, proto[, flags]]]])`

Translate the host/port argument into a sequence of 5-tuples that contains all the necessary arguments for creating a socket connected to that service.

The function returns a list of 5-tuples with the following structure:

    (family, socktype, proto, canonname, sockaddr)

where
- `family`, `socktype` and `proto` are all integers and are meant to be passed to the `socket()` function.
- `canonname` will be a string representing the canonical name of the host if `AI_CANONNAME` is part of the flags argument; else it will be `""` (empty).
- `sockaddr` is a tuple describing a socket address, whose format depends on the returned family. Example: `(address, port)` for `AF_INET`. It is meant to be passed to the `connect()` method.

### `getfqdn([name])`

Return a fully qualified domain name for `name`.

### `gethostbyname(hostname)`

Translate a hostname to IPv4 address format, returned as a string. Example: "127.0.0.1"

This does not support IPv6 name resolution, and `getaddrinfo()` should be used instead for IPv4/v6 dual stack support.


### `gethostbyname_ex(hostname)`

Translate a hostname to IPv4 address format, with **extended interface comparing to the previous method**.

It returns a triple `(hostname, aliaslist, ipaddrlist)` where
- `hostname` is the primary host name
- `aliaslist` is a (possibly empty) list of alternative host names for the same address
- `ipaddrlist` is a list of IPv4 addresses for the same interface on the same hostname.


### `gethostname()`

Return a string of the hostname of the machine where Python interpreter is currently executing.


### `gethostbyaddr(ip_address)`

Return `(hostname, aliaslist, ipaddrlist)` similar to `gethostbyname_ex`


### `getnameinfo(sockaddr, flags)`
### `getprotobyname(protocolname)`

Translate an Internet protocol name (for example, `'icmp'`) to a constant suitable for passing as the third argument to the `socket()` function. Usually only needed for sockets opened in "raw" mode (SOCK_RAW). Usually the socket is chosen automatically.


### `getservbyname(servicename[, protocolname])`

Translate an internet service name and protocol name to a port number for that service. The protocol name has to be `tcp` or `udp`. Service name, as an example, can be `"http"`.


### `getservbyport(port[, protocolname])`

Translate an Internet port number and protocol name to a service name for that service. The protocol name has to be `tcp` or `udp`. The service name corresponding to port 80 is `"http"`

### `fromfd(fd, family, type[, proto])`

Duplicate the file descriptor `fd` and build a socket object from the result. What does this do?

### `getdefaulttimeout()`

Return the default timeout in seconds (float) for new socket objects. `None` if no timeout.

### `setdefaulttimeout(timeout)`

Obvious.

### `SocketType`

This is a Python type object that represent the socket object type. Same as `type(socket(...))`



## `Socket` Objects

`Socket` object is created by `socket()` method. It has the following methods:

### `accept()`

Accept a connection. The socket must be bound to an address and listening for connections. The return value is `(conn, address)` where `conn` is a new socket object usable to send and receive data on the connection, and `address` is the address bound to the socket on the other end of the connection.

### `bind(address)`

Bind the socket to address.

### `close()`

Close the socket.

### `connect(address)`

Connect to a remote socket at address.

### `connect_ex(address)`

Just like `connect(address)`, but return an error indicator instead of raising an exception for error.

The returned value is `0` if the operation succeeded, otherwise the value of the `errno` variable. This is useful to support asynchronous connects.

### `fileno()`

Return the socket's file descriptor (a small integer). useful with `select.select()`

### `getpeername()`

Return the remote address to which the socket is connected. This is useful to find out the port number of a remote IPv4/v6 socket, for instance.

### `getsocketname()`

Return the socket's own address.

### `listen(backlog)`

Listen for connections made to the socket. The `backlog` argument specifies the maximum number of queued connections and should be at least 0; the maximum value is system-dependent (usually 5).

### `makefile([mode[, bufsize]])`

Return a file object associated with the socket. Why do we need this?

### `recv(bufsize[, flags])`

Receive data from the socket. The return value is string representing the data received. The maximum amount of data to be received at once is specified by `bufsize`. See man page `recv(2)` in Unix for the meaning of the optional argument `flags`.

### `recvfrom(bufsize[, flags])`

Similar to `recv()` but returns `(string, address)` instead of just a `string`.

### `recvfrom_into(buffer,[, nbytes[, flags]])`

Receive up to `nbytes` bytes from the socket, storing the data into a buffer rather than creating a new string. If `nbytes` is not set, receive up to the buffer length.

### `recv_into(buffer[, ntypes[, flags]])`

Similar as before.

### `send(string[, flags])`

Send data to the socket. The socket must be connected to a remote socket. Returns the number of bytes sent.

Applications are responsible for checking that all data has been sent; if only some of the data was transmitted, the application needs to attempt delivery of the remaining data.

### `sendall(string[, flags])`

Send data to the socket. But it will send all data until either all has been delivered, or an error occurs. `None` is returned on success. On error, an exception is raised, and there is no way to determine how much data was successfully sent.

### `sendto(string, address)`

Send data to the socket. The socket should **not** be connected to a remote socket, since the destination socket is specified by address. Return the number of bytes sent.

### `setblocking(flag)`

Set blocking or non-blocking mode of the socket.

- if flag is 0, the socket is set to non-blocking. Otherwise blocking.
- Initially, all sockets are in blocking mode.
- In non-blocking mode, if a `recv()` call does not find any data, or if a `send()` call can't immediately dispose of the data, an `error` exception is raised.
- In blocking mode, the calls block until they can proceed.

It's similar to `settimeout`. Non-blocking is `settimeout(0)` and blocking is `settimeout(None)`

### `settimeout(value)`

Set a timeout on blocking socket operations.

### `gettimeout()`

Obvious.

### `setsockopt(level, optname, value)`

Set the value of the given socket option (see the Unix manual page `setsockopt(2)`)

### `shutdown(how)`

Shut down one or both halves of the connection.

- If how is `SHUT_RD`, further receives are disallowed.
- If how is `SHUT_WR`, further sends are disallowed.
- If how is `SHUT_RDWR`, further sends and receives are disallowed.

### `family`, `type` and `proto`

Readonly attributes of `socket`


