with open("input.txt") as f:
    str_in = f.readline().strip()


def hex_to_bin(s):
    def char_tobin(c):
        return bin(int(c, 16))[2:].zfill(4)
    return "".join(map(char_tobin, s))


def bin_to_int(s):
    return int(s, 2)


def mul(vals):
    base = 1
    for val in vals:
        base *= val
    return base


class Packet:
    def __init__(self, ver, id):
        self.ver = bin_to_int(ver)
        self.id = bin_to_int(id)

    def bit_len(self):
        return 6

    def get_val(self):
        return 0

    def sum_ver(self):
        return self.ver


class LiteralPacket(Packet):
    def __init__(self, ver, id, val):
        super().__init__(ver, id)
        if self.id != 4:
            raise Exception("Wrong packet type lmao")
        self.val = val

    def bit_len(self):
        return 6 + len(self.val) + len(self.val) // 4

    def get_val(self):
        return bin_to_int(self.val)

    def sum_ver(self):
        return self.ver

    def sum_val(self):
        return self.get_val()


class OperatorPacket(Packet):
    def __init__(self, ver, id, maxlen, mode):
        super().__init__(ver, id)
        self.sub = []
        self.maxlen = bin_to_int(maxlen)
        self.mode = mode
        if self.id == 4:
            raise Exception("Wrong packet type lmao")

    def add_packet(self, p):
        self.sub.append(p)

    def is_full(self):
        if int(self.mode) == 1:
            return len(self.sub) >= self.maxlen
        return self.bit_len_sub() >= self.maxlen

    def bit_len_sub(self):
        return sum(map(lambda x: x.bit_len(), self.sub))

    def bit_len(self):
        return 7 + self.bit_len_sub() + (15 if self.mode == "0" else 11)

    def get_val(self):
        return None

    def sum_ver(self):
        return self.ver + sum(map(lambda x: x.sum_ver(), self.sub))

    def sum_val(self):
        op = int(self.id)
        vals = list(map(lambda x: x.sum_val(), self.sub))
        if op == 0:
            return sum(vals)
        if op == 1:
            return mul(vals)
        if op == 2:
            return min(vals)
        if op == 3:
            return max(vals)
        if op == 5:
            return 1 if vals[0] > vals[1] else 0
        if op == 6:
            return 1 if vals[0] < vals[1] else 0
        if op == 7:
            return 1 if vals[0] == vals[1] else 0
        raise Exception("What")


class Queue:
    def __init__(self, s):
        self.queue = list(s)

    def pop(self, count=1):
        s = ""
        for i in range(count):
            s += self.queue.pop(0)
        return s

    def __str__(self):
        return str(self.queue)


def parse(s):
    bits = Queue(hex_to_bin(s))
    stack = []
    while True:
        ver = bits.pop(3)
        id = bits.pop(3)
        if bin_to_int(id) == 4:
            hlt = False
            val = ""
            while not hlt:
                hlt = bits.pop() == "0"
                val += bits.pop(4)
            p = LiteralPacket(ver, id, val)
            if len(stack) == 0:
                return p
            while True:
                super_p = stack.pop()
                super_p.add_packet(p)
                if super_p.is_full():
                    if len(stack) == 0:
                        return super_p
                    p = super_p
                else:
                    stack.append(super_p)
                    break
        else:
            mode = bits.pop()
            if mode == "1":
                maxlen = bits.pop(11)
            else:
                maxlen = bits.pop(15)
            p = OperatorPacket(ver, id, maxlen, mode)
            stack.append(p)


packet = parse(str_in)
# Part 1
print(packet.sum_ver())
# Part 2
print(packet.sum_val())
