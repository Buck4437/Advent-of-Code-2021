with open("input.txt", "r") as f:
    nums = [int(line.strip()) for line in f.readlines()]


def count(size=1):
    tally = 0
    for i in range(len(nums) - size):
        if nums[i] < nums[i+size]:
            tally += 1
    return tally


# Part 1
print(count())
# Part 2
print(count(3))
