import argparse
import subprocess
import os
import helpers
import socket
import time


def poll():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatcher-server", help="dispatcher host::port, by default it uses localhost:8888",
                        default="localhost:8888", action="store")
    parser.add_argument("repo", metavar="REPO", type=str,
                        help="path to the repository this will observe")
    args = parser.parse_args()
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(":")

    while True:
        # Run update_repo.sh to grep commit id. If there is new commit id (new commit), the file .commit_id will be
        # created. Otherwise there will not be such file exists.
        try:
            # call the bash script that will update the repo and check
            # for changes. If there is a change, it will drop a .commit_id file
            # with the latest commit in the current working directory
            subprocess.check_output(["./update_repo.sh", args.repo])
        except subprocess.CalledProcessError as e:
            raise Exception("Could not update and check repository. " + " Reason: %s" % e.output)

        if os.path.isfile(".commit_id"):
            # communicate with dispatch host and make sure it's live.
            try:
                response = helpers.communicate(dispatcher_host,
                                               int(dispatcher_port),
                                               "status")
            except socket.error as e:
                raise Exception("Could not communicate with dispatcher server: %s" % e)

            # if the server is live, tell it the commit id.
            if response == "OK":
                commit = ""
                with open(".commit_id", "r") as f:
                    commit = f.readline()
                response = helpers.communicate(dispatcher_host,
                                               int(dispatcher_port),
                                               "dispatch:%s" % commit)
                if response != "OK":
                    raise Exception("Could not dispatch the test: %s" % response)
                print "dispatched!"
            else:
                raise Exception("Could not dispatch the test: %s" % response)
        time.sleep(5)
