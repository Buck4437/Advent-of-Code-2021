import time
from Day23.solver import solve

part1 = """
#############
#...........#
###A#C#B#A###
  #D#D#B#C#
  #########"""

part2 = """
#############
#...........#
###A#C#B#A###
  #D#C#B#A#
  #D#B#A#C#
  #D#D#B#C#
  #########"""

print("Program has started.")
t0 = time.time()
print(solve(part1))
print(time.time() - t0, "s")

t0 = time.time()
print(solve(part2))
print(time.time() - t0, "s")
