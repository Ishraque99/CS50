while True:
    h = int(input("Height: "))
    if (0 <= h < 23):
        break

for i in range(h):
    for j in range(h+1):
        if j < (h-i-1):
            print(" ", end="")
        else:
            print("#", end="")
    print()
