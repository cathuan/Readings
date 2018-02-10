import argparse
import threading
import time
import socket
import helpers
import SocketServer
import re
import os


"""
The TCPServer we are using is actuall inside the builtin module SocketServer, which is pretty
simple. But it has one problem: it can communicate with only one connection at once.

So when it communicates with a runner, it won't be able to communicate with repo observer,
which is not good enough.

We use ThreadingTCPServer to handle this problem, by adding threading ability to the
default SocketServer.
This means that any time the dispatcher receives a connection request, it spins off a new
process just for that connection.
"""
class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    runners = []  # keeps track of test runner pool
    dead = False  # indicate to other threads that we are no longer running
    dispatched_commits = {}  # keeps track of commits we dispatched
    pending_commits = []  # keeps track of commits we have yet to dispatch


class DispatcherHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our dispatcher.
    This will dispatch test runners against the incoming commit and handle
    their requests and test results
    """
    command_re = re.compile(r"(\w+)(:.+)*")
    BUF_SIZE = 1024

    def handle(self):
        self.data = self.request.recv(self.BUF_SIZE).strip()
        command_groups = self.command_re.match(self.data)
        if not command_groups:
            self.request.sendall("Invalid command")
            return
        command = command_groups.group(1)

        if command == "status":
            print "in status"
            self.request.sendall("OK")
        elif command == "register":
            # Add this test runner to our pool
            print "register"
            address = command_groups.group(2)
            host, port = re.findall(r":(\w*)", address)
            runner = {"host": host, "port": port}
            self.server.runners.append(runner)
            self.request.sendall("OK")
        elif command == "dispatch":
            print "going to dispatch"
            commit_id = command_groups.group(2)[1:]
            if not self.server.runners:
                self.request.sendall("No runners are registered")
            else:
                # The coordinator can trust us to dispatch the test
                self.request.sendall("OK")
                dispatch_tests(self.server, commit_id)
        elif command == "results":
            print "got test results"
            results = command_groups.group(2)[1:]
            results = results.split(":")
            commit_id = results[0]
            length_msg = int(results[1])
            # 3 is the number of ":" in the sent command
            remaining_buffer = self.BUF_SIZE - \
                (len(command) + len(commit_id) + len(results[1]) + 3)
            if length_msg > remaining_buffer:
                self.data += self.request.recv(length_msg - remaining_buffer).strip()
            del self.server.dispatched_commits[commit_id]
            if not os.path.exists("test_results"):
                os.makedirs("test_results")
            with open("test_results/%s" % commit_id, "w") as f:
                data = self.data.split(":")[3:]
                data = "\n".join(data)
                f.write(data)
            self.request.sendall("OK")


# check whether the runners in server is alive.
# If not, remove the runner and put the commit id task the runner performs in the pending list
# It checks two things:
#   - socket connection to the runner fails
#   - ping the runner but didn't receive the response or the response is not "pong" (OK)
def runner_checker(server):
    def manage_commit_lists(runner):
        for commit, assigned_runner in server.dispatched_commits.iteritems():
            if assigned_runner == runner:
                del server.dispatched_commits[commit]
                server.pending_commits.append(commit)
                break
        server.runners.remove(runner)

    while not server.dead:
        time.sleep(1)
        for runner in server.runners:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                response = helpers.communicate(runner["host"], int(runner["port"]), "ping")
                if response != "pong":
                    print "removing runner %s" % runner
                    manage_commit_lists(runner)
            except socket.error:  # as e
                manage_commit_lists(runner)


def redistribute(server):
    while not server.dead:
        for commit in server.pending_commits:
            print "Running redistribute"
            print server.pending_commits
            dispatch_tests(server, commit)
            time.sleep(5)


# Find an available test runner from the pool of registered runners.
# Allocate a test with commit_id to an available runner
def dispatch_tests(server, commit_id):
    # NOTE: usually we don't run this forever
    while True:
        print "Trying to dispatch to runners"

        # Try to find a free runner by sending request to the runner server asking whether it
        # can run the commit id test task.

        # If we find an available runner, dispatch to it and remove the commit id from the
        # pending list if it is in, and return. The task is finished.
        for runner in server.runners:
            response = helpers.communicate(runner["host"], int(runner["port"]),
                                           "runtest:%s" % commit_id)
            if response == "OK":
                print "adding id %s" % commit_id
                server.dispatched_commits[commit_id] = runner
                if commit_id in server.pending_commits:
                    server.pending_commits.remove(commit_id)
                return

        # if none of the runner is available, we come back and ask again after 2 seconds.
        time.sleep(2)


def serve():

    parser = argparse.ArgumentParse()
    parser.add_argument("--host", help="dispatcher's host, by default it uses localhost",
                        default="localhost", action="store")
    parser.add_argument("--port", help="dispatcher's port, by default it uses 8888",
                        default=8888, action="store")
    args = parser.parse_args()

    # starts the dispatcher server, and two other threads.
    # One thread runs `runner_checker` function
    # The other one runs the `redistribute` function

    server = ThreadingTCPServer((args.host, int(args.port)), DispatcherHandler)
    print "serving on %s:%s" % (args.host, int(args.port))

    """......"""

    runner_heartbeat = threading.Thread(target=runner_checker, args=(server,))
    redistributor = threading.Thread(target=redistribute, args=(server,))

    try:
        runner_heartbeat.start()
        redistributor.start()
        # Activate the server; this will keep running until user interrupts
        server.serve_forever()
    except (KeyboardInterrupt, Exception):
        # if any exception occurs, kill the thread
        server.dead = True
        runner_heartbeat.join()
        redistributor.join()
