# What is a Continuous Integration System?

The continuous integration (CI) systems are dedicated systems used to test new codes.
- Upon a commit to the repository, the system will test all the codes won't break any test.
- The system will fetch the changes, run the tests and report its results.
- The system is failure resistant.
- The system should be able to run the test in parallel so developers can achieve the results of the tests in a reasonable amount of time.

# Project Limitations and Notes

The project
- Uses `Git` as the version control repository
- Only run tests that are in the directory named `tests` within the repository
- Use local repository instead of web server
- CI runs periodically in the example. Actually CI can run per commit base.
- This system gathers the result and save them in files in the file system local to the dispatcher process

# Introduction

The basic structure of a CI system consists three components:
- An observer: watches the repository and notifies the job dispatchers there is a new commit
- A test job dispatcher: finds a test runner and give it the commit number to test
- A test runner: run the test

There are many possible architectures for the CI system
- All three components can be on the same machine, but it
    - has no load handling, and the capacity is limited (not load-bearing)
    - if the machine is down, no tests will be run (not failt-tolarent)
- Each components will be run on different process
- They communicate via sockets, so they can be run on different network machines

With this architecture, all three components are run on different machine. So if any of the components are down, we can schedule a new machine, and run the buffered tasks after the new machine is up. It also allows us run multiple tests in parallel. (Distributed system? I reckon this does not require too many locks, as we generally don't have data race.)

The project does **not** have auto-recovery code as it is independent on the distributed system's architecture.

## Files in this Project

In this project, we have one Python file for each component:
- the repository observer `repo_observer.py`
- the test job dispatcher `dispatcher.py`
- the test runner `test_runner.py`
- the communicator `helper.py`

Each of these three processes communicate with each other using sockets using `helper.py`.

There are also bash scripts to help python to run system level of jobs instead of using `os` and `subprocess`.

Lastly, there is a tests directory containing all the tests.


# The Components

## The Repository Observer (`repo_observer.py`)


