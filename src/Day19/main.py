from Day19.scanner import Scanner

with open("input.txt") as f:
    ln = f.readline()
    scanners = []
    sc_id, ords = None, []
    while ln != "":
        if ln == "\n":
            scanners.append(Scanner(sc_id, ords))
            sc_id = None
            ords = []
        elif ln.find("---") != -1:
            sc_id = int(ln[12:].replace("---", "").strip())
        else:
            ords.append([int(n) for n in ln.strip().split(",")])
        ln = f.readline()
    if len(ords) != 0:
        scanners.append(Scanner(sc_id, ords))


# for s in scanners:
#     print(s)

import time
t0 = time.time()
num = 0
scanners[0].identify_pos(scanners[2])
print(time.time() - t0)

known = [scanners[0]]
unknown = set(scanners[1:])
while len(unknown) != 0:
    cur_scn = known.pop(0)
    new = []
    for ukn_sc in unknown:
        if cur_scn.identify_pos(ukn_sc):
            new.append(ukn_sc)
            print(f"{ukn_sc.id} identified with {cur_scn.id}")
        else:
            print(f"{ukn_sc.id} failed with {cur_scn.id}")
    known = known + new
    for n in new:
        unknown.remove(n)

beacons = set()
for sc in scanners:
    ords = sc.get_ords_abs()
    for coord in ords:
        beacons.add(coord)
print(len(beacons))

max_dst = 0
for i in range(len(scanners)):
    for j in range(i+1, len(scanners)):
        max_dst = max(max_dst, scanners[i].dst(scanners[j]))

print(max_dst)