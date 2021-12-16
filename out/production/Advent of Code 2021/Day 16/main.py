with open("input.txt") as f:
    str_in = f.readline().strip()


def hex_to_bin(s):
    def char_tobin(c):
        return bin(int(c, 16))[2:].zfill(4)
    return "".join(map(char_tobin, s))


def bin_to_int(s):
    return int(s, 2)


class Packet:
    def __init__(self, ver, id):
        self.ver = bin_to_int(ver)
        self.id = bin_to_int(id)

    def bit_len(self):
        return 6

    def get_val(self):
        return 0


class LiteralPacket(Packet):
    def __init__(self, ver, id, val):
        super().__init__(ver, id)
        if self.id != 4:
            raise Exception("Wrong packet type lmao")
        self.val = val

    def bit_len(self):
        return 6 + len(self.val)

    def get_val(self):
        return bin_to_int(self.val)

    def tostr(self):
        return "LitPacket" + str(self.get_val()) + "Length" + str(self.bit_len())

    def __str__(self):
        return self.tostr()


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
        if int(self.mode) == "1":
            return len(self.sub) >= self.maxlen
        print(self.bit_len_sub())
        return self.bit_len_sub() >= self.maxlen

    def bit_len_sub(self):
        return sum(map(lambda x: x.bit_len(), self.sub))

    def bit_len(self):
        return 7 + self.bit_len_sub()

    def get_val(self):
        return None

    def tostr(self):
        return "OpPacket" + "{" + str(list(map(lambda x: x.tostr(), self.sub))) + "}" + "Length" + str(self.bit_len()) + "Mode" + self.mode

    def __str__(self):
        return self.tostr()


class Queue:
    def __init__(self, s):
        self.stack = list(s)

    def pop(self, count=1):
        s = ""
        for i in range(count):
            s += self.stack.pop(0)
        return s

    def __str__(self):
        return str(self.stack)


def parse(s):
    print(hex_to_bin(s))
    bits = Queue(hex_to_bin(s))
    stack = []
    while True:
        ver = bits.pop(3)
        id = bits.pop(3)
        print("ver", ver, "id", id)
        if bin_to_int(id) == 4:
            hlt = False
            val = ""
            while not hlt:
                hlt = bits.pop() == "0"
                val += bits.pop(4)
            print("val", val)
            p = LiteralPacket(ver, id, val)
            print(p)
            if len(stack) == 0:
                return p
            while True:
                super_p = stack.pop()
                super_p.add_packet(p)
                print(super_p)
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
print(packet)