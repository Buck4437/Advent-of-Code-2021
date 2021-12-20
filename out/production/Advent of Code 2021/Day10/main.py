with open("input.txt", "rt") as f:
    nvs = [s.strip() for s in f.readlines()]

brackets = "([{<)]}>"
points = 0
error_point = [3, 57, 1197, 25137]
scores = []
for nv in nvs:
    stack = []
    for c in nv:
        idx = brackets.find(c)
        if idx < 4:
            stack.append(idx)
        elif stack.pop() != idx - 4:
            points += error_point[idx - 4]
            break
    else:
        score = 0
        while len(stack) > 0:
            score = score * 5 + stack.pop() + 1
        scores.append(score)

# Part 1
print(points)
# Part 2
print(sorted(scores)[len(scores) // 2])
