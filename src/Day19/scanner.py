# Default direction: Facing +ve x, +ve y as top
def rotate(coord, direction=0):
    x, y = coord
    if direction == 0:
        return [x, y]
    if direction == 1:
        return [y, -x]
    if direction == 2:
        return [-x, -y]
    return [-y, x]


def rotate3d(coord, direct=0):
    d1, d2 = direct // 4, direct % 4
    x, y, z = coord
    if d1 == 0:
        return [x] + rotate([y, z], d2)
    if d1 == 1:
        return [-x] + rotate([z, y], d2)
    if d1 == 2:
        return [y] + rotate([z, x], d2)
    if d1 == 3:
        return [-y] + rotate([x, z], d2)
    if d1 == 4:
        return [z] + rotate([x, y], d2)
    if d1 == 5:
        return [-z] + rotate([y, x], d2)
    raise Exception("no")


def dst(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return max(x1, x2) + max(y1, y2) + max(z1, z2) - (min(x1, x2) + min(y1, y2) + min(z1, z2))


def vec_add(c1, c2):
    x0, y0, z0 = c1
    x1, y1, z1 = c2
    return x0 + x1, y0 + y1, z0 + z1


def vec_minus(c1, c2):
    x0, y0, z0 = c1
    x1, y1, z1 = c2
    return x0 - x1, y0 - y1, z0 - z1


class Scanner:
    def __init__(self, sc_id, ords):
        self.id = sc_id
        self.ords = ords
        self.dir = 0 if sc_id == 0 else None
        self.pos = [0, 0, 0] if sc_id == 0 else None
        self.cache_abs = None

    def __str__(self):
        return f"Scanner {self.id}: facing direction {self.dir}"

    def get_ords(self, pos, direction):
        return [vec_add(pos, rotate3d(coord, direction)) for coord in self.ords]

    def get_ords_abs(self):
        if self.cache_abs is None:
            self.cache_abs = self.get_ords(self.pos, self.dir)
        return self.cache_abs

    def identify_pos(self, s2):
        if self.dir is None and self.pos is None:
            print(f"Scanner{self.id}'s pos and dir is unknown, choose something else as the base")
            return -1
        for direction in range(24):
            fixed, target = self.get_ords_abs(), [rotate3d(coord, direction) for coord in s2.ords]
            for o1 in fixed:
                for o2 in target:
                    pp = vec_minus(o1, o2)
                    ords2 = {vec_add(pp, vec) for vec in target}
                    if len(set(fixed) & ords2) >= 12:
                        s2.pos = pp
                        s2.dir = direction
                        return True
        return False

    def dst(self, sc2):
        return dst(self.pos, sc2.pos)