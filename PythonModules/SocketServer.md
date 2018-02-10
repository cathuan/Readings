# SocketServer builtin module

## Introduction

The source code is in Lib/SocketServer.py of CPython repo.

There are four basic classes in the module

### `TCPServer`

The constructor is

    SocketServer.TCPServer(server_address, RequestHandlerClass, bind_and_activate=True)

which uses the internet **TCP protocol, provides continuous streams of data between the client and server**.

### `UDPServer`

The constructor is

    SocketServer.UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)

which usses datagrams, i.e. discrete packets of information that may arrive out of order or be lost while in transit.

### `UnixStreamServer` and `UnixDatagramServer`

These two more infrequently used classes are similar to `TCPServer` and `UDPServer`, instead they are using UNIX domain sockets, which are not available for Non-Unix platform.

### Synchronous handles

These classes process requests *synchronously*. Each request must be completed before the next request can be started.The solution is to create separate process or thread to handle each request. The `ForingMixIn` and `ThreadingMixIn` classes can be used to support asynchronous behavior.

### Steps to create a server

Creating a server requires several steps:

- Create a request handler class by subclassing the `BaseRequestHandler` class and overriding its `handle()` method.
- Instantiate one of the server classes, and passing it the server's address and the request class.
- Call the `handle_request()` or `server_forever()` method of the server object to process one/many requests.
- Call `server_close()` to close the socket.


## Server Creation Notes

There are five classes in an inheritance diagram, and four of which represent synchronous servers:

        +------------+
        | BaseServer |
        +------------+
              |
              v
        +-----------+        +------------------+
        | TCPServer |------->| UnixStreamServer |
        +-----------+        +------------------+
              |
              v
        +-----------+        +--------------------+
        | UDPServer |------->| UnixDatagramServer |
        +-----------+        +--------------------+

The steps of creating a server is in the last subsection.


## Server Objects

### `BaseServer`

This class is the superclass of all Server objects in the module. It defines the interface but does not implement most of the methods, which should be done in subclasses. The constructor gets two params and store them in `server_address` and `RequestHandlerClass` attributes.

#### `address_family`

The family of protocols to which the server's socket belongs. Common examples are `socket.AF_INET` and `socket.AF_UNIX`

#### `RequestHandlerClass`

User provided handler class. An instance will be initialized for each request. *(maybe inefficiency?)*

#### `server_address`

The address on which the server is listening. Example: `('127.0.0.1', 80)`

#### `socket`

The **socket object** on which the server will listen for incoming requests.

#### `fileno()`

Return an integer file descriptor for the socket on which the server is listening.

#### `handle_request()`

Process a single request. This function calls the following methods in order:

- `get_request()`
- `verify_request()`
- `process_request()`

If the user-provided `handle()` method of the handler class raises an exception, the server's `handle_error()` method will be called.

If no request is received within `timeout` seconds, `handle_timeout()` will be called and `handle_request()` will return.


#### `server_forever(poll_interval=0.5)`

- Handle requests until an explicit `shutdown()` request.
- Poll for `shutdown` every `poll_interval` seconds.
- Ignore `timeout` attribute

#### `shutdown()`

Tell the `serve_forever()` loop to stop and wait until it does.

#### `server_close()`

Clean the server and may be overriden.

#### `allow_reuse_address`

Whether the server will allow the reuse of an address. Defaults to `False`, and can be set in subclasses to change the policy.

#### `request_queue_size`

The size of the request queue. Any requests that arrive while the server is busy are placed into a queue, up to `request_queue_size` requests. Once the queue is full, further request will get "Connection denied" error. The default value is usually 5.

#### `socket_type`

The type of socket used by the server. Common values are `socket.SOCK_STREAM` and `socket.SOCK_DGRAM`.

#### `timeout`

Timeout duration, measured in seconds. If `handle_request()` receives no incoming request within the timeout period, `handle_timeout()` method is called.

#### `finish_request(request, client_address)`

**Actually** processes the request by instantiating `RequestHandlerClass` and calling its `handle()` method.

#### `get_request()`

Must accept a request from the socket, and return a 2-tuple containing the _new_ socket object to be used to communicate with the client, and the client's address.

#### `handle_error(request, client_address)`

#### `handle_timeout()`

#### `process_request(request, client_address)`

Calls `finish_request()` to create an instance of the `RequestHandlerClass`. If desired, this function can create a new process or thread to handle the request; the `ForkingMixIn` and `ThreadingMixIn` classes do this.

#### `server_activate()`

#### `server_bind()`

Called by the server's constructor to bind the socket to the desired address. May be overridden.

#### `verify_request(request, client_address)`

Must return a Boolean value; if the value is `True`, the request will be processed, and if it's `False`, the request will be denied. This function can be overridden to implement access controls for a server. The default implementation always return `True`.


## Request Handler Objects

### `BaseRequestHandler`

The base class of Request Handler Objects is `BaseRequestHandler`. A new subclass must implement `handle()` method.

#### `setup()`

Called before the `handle()` method to perform any initialization actions required. The default implementation does nothing.

#### `handle()`

The function **must** do all the work required to service a request. The default implementation does nothing. Several instance attributes are available.
- the request is `self.request`
- the client address is `self.client_address`
- the server instance as `self.server`

The type of request is different for datagram or stream services.
- For stream services, `self.request` is a socket object.
- For datagram services, `self.request` is a pair of string and socket.

#### `finish()`

Called after the `handle()` method to perform any clean-up actions required. The default implementation does nothing.

If `setup()` raises an exception, `finish()` will not be called.

### `StreamRequestHandler` and `DatagramRequestHandler`

These subclasses of `BaseRequestHandler` override the `setup()` and `finish()` methods, and provide `self.rfile` and `self.wfile` attributes.

The new attributes can be read or written, respectively, to get the request data or return data to the client.
