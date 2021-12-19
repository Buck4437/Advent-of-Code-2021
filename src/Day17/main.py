def sgn(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


tx, ty = (94, 151), (-156, -103)
hits = 0
max_height = 0
for vxi in range(tx[1] + 1):
    for vyi in range(ty[0], -ty[0] + 2):
        px, py = 0, 0
        vx, vy = vxi, vyi
        max_h = 0
        while True:
            px, py = px + vx, py + vy
            vx, vy = vx - sgn(vx), vy - 1
            max_h = max(max_h, py)
            if tx[0] <= px <= tx[1] and ty[0] <= py <= ty[1]:
                max_height = max(max_height, max_h)
                hits += 1
                break
            if px > tx[1] or py < ty[0]:
                break
print(max_height)
print(hits)
