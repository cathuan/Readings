# Introduction

We introduce the fundamental structure of an Python interpreter `Byterun` which fits easily into the 500-line size restriction.

The structure is similar to the primary implementation of Python, CPython. So understanding `Byterun` will help you understand interpreters in general and the CPython interpreter in particular.

## A Python Interpreter

Interpreter means different things under different context. Here we narrow it down to mean __the last step in the process of executing a Python program__.

Before the interpreter takes over, Python performs three other steps:
- lexing
- parsing
- compiling

The processes transform the programmer's source code from lines of text into structured `code objects` containing instructions that the interpreter can understand. __The interpreter's job is to take these code objects and follow the instructions__.

Here is an interesting fact: most interpreted language, including Python, do involve a compilation step. But the compilation step does relative less work (and the interpreter does relatively more).

## A Python Python Interpreter

Writing a Python interpreter in Python has both advantages and disadvantages.
- The biggest disadvantage is speed. But `Byterun` is designed as a learning process so speed is not the main concern.
- The biggest advantage is that we can easily implement _just_ the interpreter, and not the rest of the Python run-time, particularly the object system.
- Another advantages is `Byterun` is easy to understand.

# Building an Interpreter

First we need some higher-level context on the structure of the interpreter.

The Python interpreter is a _virtual machine_. This particular virtual machine is a stack machine: it manipulates several stacks to perform its operations (as contrasted with a register machine, which writes to and reads from particular memory locations).

The Python interpreter is a _bytecode interpreter_: its input is instruction sets called _bytecode_. Each code object contains a set of instructions to be executed -- called bytecode -- plus other information that the interpreter will need.

Bytecode is an _intermediate representation_ of Python code: it expresses the source code that you wrote in a way the interpreter can understand.

## A Tiny Interpreter

We start with a very minimal interpreter.
- This interpreter can only add numbers
- It only understands three instructions
    - `LOAD_VALUE`
    - `ADD_TWO_VALUES`
    - `PRINT_ANSWER`

Suppose we want to operate `7+5`, we produce the instruction set

    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("LOAD_VALUE", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [7, 5]
    }

The `LOAD_VALUE` instruction tells the interpreter to push a number on to the stack, but the instruction alone does not specify which number. Each instruction needs an extra piece of information, telling the interpreter where to find the number to load.

In Python, what we're calling "instructions" is the bytecode, and the "what_to_execute" object is the _code object_.

### Why not put the numbers directly in the instructions?

Imagine if we were adding strings together instead of numbers. We would not want strings in the instructions, since they can be arbitrary long.

The design also means we can have just one copy of each object that we need. So if we do `7+7`, the numbers will be just `[7]`.

### Interpreter

Now we start to write the interpreter itself. The code is in `interpreter.py`.
