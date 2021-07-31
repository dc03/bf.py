(
    # `sys` represents the module `sys`
    lambda sys: (
        # `exec_state` represents the state of the interpreter, explained below
        lambda exec_state: (
            # `insn_dict` represents the mapping from brainfuck instructions to lambdas that contain code to represent
            # what they actually do
            lambda insn_dict: [
                # Unpacking the `iter` into a list forces evaluation, thus this is a good way to represent `while` loops
                *iter(
                    (
                        # Here, the lambda is used as a way to sequence expressions to happen after one another, as
                        # lists are evaluated from left to right
                        lambda: [
                            # The loop condition
                            exec_state[2] < len(exec_state[0]),
                            # If we are within the bounds of the code, and we have an instruction, find its appropriate
                            # mapping in `insn_dict`, and execute it
                            insn_dict[exec_state[0][exec_state[2]]]()
                            if exec_state[2] < len(exec_state[0])
                            and exec_state[0][exec_state[2]] in insn_dict.keys()
                            else None,
                            # Increment the code pointer to point to the next character in the code
                            exec_state.update({2: exec_state[2] + 1}),
                        ][0] # Return the loop condition
                    ),
                    # Iterate until the loop condition is false
                    False,
                )
            ]
        )(
            # The dictionary which defines the mapping of brainfuck instructions to actual code
            {
                # Increment the byte pointer, wrapping at 30,000 back to 0, the start of the byte array
                ">": (lambda: exec_state.update({4: (exec_state[4] + 1) % 30000})),
                # Decrement the byte pointer, wrapping below 0 to 29,999, the end of the byte array
                "<": (
                    lambda: exec_state.update(
                        {4: (exec_state[4] - 1) if exec_state[4] else 29999}
                    )
                ),
                # Handle loop instructions. If the current byte being pointed to by the byte pointer is 0, skip this
                # loop and any loops it may contain by calling the lambda located at `exec_state[5]`. Otherwise, append
                # the current code pointer to the execution stack `exec_state[1]`, so that it can be jumped back to
                # later
                "[": (
                    lambda: exec_state.update(
                        {
                            # In both cases, we set the code pointer. When the current byte is not 0, do nothing. If it
                            # is 0, the lambda returns the value of the code pointer at the next instruction to be
                            # executed, and the code pointer is set to that.
                            #
                            # Note that however, as the lambda itself modifies the code pointer to point to the next
                            # instruction, this is not strictly necessary
                            2: (exec_state[1].append(exec_state[2]), exec_state[2])[1]
                            if exec_state[3][exec_state[4]]
                            else exec_state[5](exec_state)
                        }
                    )
                ),
                # Handle loop ends. This one is much simpler: if the current byte is not 0, set the code pointer to the
                # top of the execution stack, otherwise pop the top of the execution stack and do nothing
                "]": (
                    lambda: exec_state.update(
                        {
                            2: exec_state[1][-1]
                            if exec_state[3][exec_state[4]]
                            else (exec_state[1].pop(), exec_state[2])[1]
                        }
                    )
                ),
                # Increment the current byte, wrapping back to 0 when it is 256, representing modulo arithmetic on an
                # unsigned byte
                "+": (
                    lambda: exec_state[3].__setitem__(
                        exec_state[4], (exec_state[3][exec_state[4]] + 1) & 255
                    )
                ),
                # Decrement the current byte, wrapping back to 255 when it is less than zero
                "-": (
                    lambda: exec_state[3].__setitem__(
                        exec_state[4],
                        exec_state[3][exec_state[4]] - 1
                        if exec_state[3][exec_state[4]]
                        else 255,
                    )
                ),
                # Read the current byte as a character from stdin
                ",": (
                    lambda: exec_state[3].__setitem__(
                        exec_state[4], ord(sys.stdin.read(1))
                    )
                ),
                # Print the current byte as a character to stdout
                ".": (lambda: print(chr(exec_state[3][exec_state[4]]), end="")),
            },
        )
    )(
        {
            # This dictionary represents the main state of the interpreter
            # ------------------------------------------------------------
            # The string representing the input code
            0: open(sys.argv[1]).read(),
            # The execution stack which represents where various '['s are located so that they can be jumped back to
            1: [],
            # The pointer/index into the code string representing the current instruction being executed
            2: 0,
            # The byte array which represents the memory tape allocated to the interpreter
            3: [0] * 30000,
            # The pointer/index into the byte array which represents the byte currently being modified
            4: 0,
            # The lambda function used to jump over (possibly) nested loops, [], when the loop condition is false
            5: (
                lambda exec_state: (
                    # Jump to the next character in the code
                    exec_state.update({2: exec_state[2] + 1}),
                    [
                        # Iterate until we hit a ']', indicating the end of the lop
                        *iter(
                            (
                                # This code can be represented as:
                                #
                                # 1. while code[code_pointer] != "]":
                                # 2.     if code[code_pointer] == "[":
                                # 3.         skip_loop()
                                # 4.     code_pointer += 1
                                #
                                # Line number (4.) in this case is only executed when `code[code_pointer]` is not `"]"`.
                                # However, calling `skip_loop()` can alter the `code_pointer`, so this condition
                                # might not remain true when we get to line (4.). Thus, it is stored in the `state`
                                # variable of the lambda.
                                #
                                # This value of the `state` variable is then checked when updating the code pointer.
                                lambda state={0: False}: (
                                    # The loop condition
                                    exec_state[0][exec_state[2]] != "]",
                                    # Set the value of `state`
                                    state.update(
                                        {0: exec_state[0][exec_state[2]] != "]"}
                                    ),
                                    # If we have a "[" in the input, it indicates a nested loop that has to be jumped
                                    # over.
                                    exec_state[5](exec_state)
                                    if exec_state[0][exec_state[2]] == "["
                                    else None,
                                    # As the above line can update the value of `code_pointer`, check against the
                                    # `state` variable
                                    exec_state.update({2: exec_state[2] + 1})
                                    if state[0]
                                    else None,
                                )[0] # Return the loop condition
                            ),
                            False,
                        )
                    ],
                    # Return the current code pointerr
                    exec_state[2],
                )[-1]
            ),
        }
    )
    if len(sys.argv) > 1
    else print(f"Usage: {sys.argv[0]} FILE")
)(__import__("sys"))
