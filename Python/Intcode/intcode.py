def mul(li):
    if len(li) == 0:
        return None
    if len(li) == 1:
        return li[0]
    m = li[0]
    for i in li[1:]:
        m *= i
    return m


class IntcodeException(Exception):
    pass


class IntcodeSyntaxError(IntcodeException):
    pass


class UnknownOpcode(IntcodeException):
    pass


class Intcode:
    EEXIT = 0
    EINPUT = 1

    def __init__(self, source):
        self.source = source
        self.memory = []
        for op in self.source.split(","):
            try:
                self.memory.append(int(op))
            except ValueError:
                raise IntcodeSyntaxError("Error when parsing the following instruction: \"" + op + "\"")
        self.inputs = []
        self.outputs = []
        self.pointer = 0
        self.ops = {
            1: self.op_add,
            2: self.op_mul,
            3: self.op_input,
            4: self.op_output,
            5: lambda mode: self.op_jmp(mode, non_zero=True),
            6: lambda mode: self.op_jmp(mode, non_zero=False),
            7: self.op_lt,
            8: self.op_eq,
            99: lambda mode: Intcode.EEXIT
        }

    def reset(self):
        self.inputs = []
        self.outputs = []
        self.pointer = 0
        self.memory = []
        for op in self.source.split(","):
            try:
                self.memory.append(int(op))
            except ValueError:
                raise IntcodeSyntaxError("Error when parsing the following instruction: \"" + op + "\"")

    def move_pointer(self, val):
        self.pointer += val

    def set_pointer(self, val):
        self.pointer = val

    def get_val(self, val, mode=0):
        return self.get_vals([val], [mode])[0]

    def get_vals(self, val, modes=None):
        if modes is None:
            modes = []
        params = []
        for i in range(len(val)):
            if len(modes) <= i or modes[i] == 0:
                params.append(self.memory[val[i]])
            elif modes[i] == 1:
                params.append(val[i])
        return params

    def next_param(self):
        return self.next_params(1)[0]

    def next_params(self, number):
        params = self.get_vals([i for i in range(self.pointer, self.pointer + number)])
        self.move_pointer(number)
        return params

    def next_op(self):
        op = self.next_param()
        opcode = op % 100
        modes_int = op // 100
        modes = []
        while modes_int > 0 or len(modes) == 0:
            modes.append(modes_int % 10)
            modes_int //= 10
        return {
            "code": opcode,
            "modes": modes
        }

    def put(self, pos, val):
        self.memory[pos] = val

    def input(self, inputs):
        self.inputs += inputs

    def run(self):
        while True:
            op = self.next_op()
            opcode = op["code"]
            try:
                func = self.ops[opcode]
            except KeyError:
                raise UnknownOpcode("Unknown opcode: " + str(opcode))
            exit_code = func(op["modes"])
            if exit_code is not None:
                return exit_code

    def op_add(self, modes):
        params = self.next_params(3)
        val = sum(self.get_vals(params[:-1], modes))
        self.put(pos=params[-1], val=val)

    def op_mul(self, modes):
        params = self.next_params(3)
        val = mul(self.get_vals(params[:-1], modes))
        self.put(pos=params[-1], val=val)

    def op_input(self, modes):
        if len(self.inputs) == 0:
            self.move_pointer(-1)
            return Intcode.EINPUT
        val = self.inputs.pop(0)
        param = self.next_param()
        self.put(pos=param, val=val)

    def op_output(self, modes):
        param = self.next_param()
        val = self.get_val(param, modes[0])
        self.outputs.append(val)

    def op_jmp(self, modes, non_zero):
        params = self.next_params(2)
        vals = self.get_vals(params, modes)
        if (non_zero and vals[0] != 0) or ((not non_zero) and vals[0] == 0):
            self.set_pointer(vals[1])

    def op_lt(self, modes):
        params = self.next_params(3)
        vals = self.get_vals(params, modes)
        self.put(pos=params[2], val=1 if vals[0] < vals[1] else 0)

    def op_eq(self, modes):
        params = self.next_params(3)
        vals = self.get_vals(params, modes)
        self.put(pos=params[2], val=1 if vals[0] == vals[1] else 0)


try:
    intcode = Intcode("3,225,1,225,6,6,1100,1,238,225,104,0,1101,65,39,225,2,14,169,224,101,-2340,224,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1001,144,70,224,101,-96,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,92,65,225,1102,42,8,225,1002,61,84,224,101,-7728,224,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,67,73,224,1001,224,-4891,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1102,54,12,225,102,67,114,224,101,-804,224,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,19,79,225,1101,62,26,225,101,57,139,224,1001,224,-76,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1102,60,47,225,1101,20,62,225,1101,47,44,224,1001,224,-91,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1,66,174,224,101,-70,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,226,224,102,2,223,223,1005,224,329,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,374,1001,223,1,223,1108,226,677,224,1002,223,2,223,1005,224,389,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,419,1001,223,1,223,1008,226,677,224,102,2,223,223,1005,224,434,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,108,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,569,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,584,101,1,223,223,1107,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,629,1001,223,1,223,107,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,677,224,102,2,223,223,1006,224,659,101,1,223,223,1008,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226")
    intcode.reset()
    while True:
        exit_code = intcode.run()
        if exit_code == Intcode.EINPUT:
            intcode.input([int(input())])
        else:
            break
    print(intcode.outputs)
except IntcodeException as e:
    print(e)
