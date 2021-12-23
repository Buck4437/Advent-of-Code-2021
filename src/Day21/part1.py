import time
t0 = time.time()


def dice_gen():
    roll = 0
    while True:
        yield roll + 1
        roll = (roll + 1) % 100


pos1, pos2 = 4 - 1, 7 - 1
score1 = score2 = 0
p1_turn = True
roll_count = 0
dice = dice_gen()

while score1 < 1000 and score2 < 1000:
    total = 0
    for i in range(3):
        total += next(dice)
    roll_count += 3
    if p1_turn:
        pos1 = (pos1 + total) % 10
        score1 += pos1 + 1
    else:
        pos2 = (pos2 + total) % 10
        score2 += pos2 + 1
    p1_turn = not p1_turn
print(min(score1, score2) * roll_count)


print(time.time() - t0, "s")