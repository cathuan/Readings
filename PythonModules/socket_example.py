import socket


# Server echo
# Return the data received by server (from remote socket) back to the remote socket.
def server_echo():

    HOST = "localhost"  # Symbolic name meaning all available interfaces
    PORT = 50007  # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print "Connected by", addr
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print "Receive data from %s: %s" % (addr, data)
        conn.sendall(data)
    conn.close()


def client_echo():

    HOST = socket.gethostbyname("localhost")
    PORT = 50007

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall("Hello, world")
    data = s.recv(1024)
    s.close()
    print "Received", repr(data)


"""
Run server_echo() in one terminal, and run client_echo() in another terminal.
"""

if __name__ == "__main__":

    client_echo()
