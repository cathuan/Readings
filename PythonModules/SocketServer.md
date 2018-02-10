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
