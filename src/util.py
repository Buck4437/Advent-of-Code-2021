def display(set, fill="#", space=" "):
    x_mx, y_mx = max(map(lambda x: x[0], set)), max(map(lambda x: x[1], set))
    x_mn, y_mn = min(map(lambda x: x[0], set)), min(map(lambda x: x[1], set))
    for j in range(y_mn, y_mx + 1):
        for i in range(x_mn, x_mx + 1):
            print(fill if (i, j) in set else space, end="")
        print()
