from collections import defaultdict
import time
t0 = time.time()

rolls = defaultdict(int)
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            rolls[i + j + k] += 1

win1 = win2 = 0
p1_turn = True
states = {(0, 0, 4 - 1, 7 - 1): 1}
while len(states) != 0:
    new = defaultdict(int)
    for state in states:
        universes = states[state]
        for roll in rolls:
            score1, score2, pos1, pos2 = state
            multiplier = rolls[roll]
            if p1_turn:
                pos1 = (pos1 + roll) % 10
                score1 += pos1 + 1
                if score1 >= 21:
                    win1 += universes * multiplier
                    continue
            else:
                pos2 = (pos2 + roll) % 10
                score2 += pos2 + 1
                if score2 >= 21:
                    win2 += universes * multiplier
                    continue
            new[(score1, score2, pos1, pos2)] += universes * multiplier
    states = new
    p1_turn = not p1_turn

print(max(win1, win2))
print(time.time() - t0, "s")
