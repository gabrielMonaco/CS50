from cs50 import get_int

# ask height
height = get_int("Height: ")
while height <= 0 or height >= 9:
    height = get_int("Height: ")
# number os spaces and blocks in first line
space = height - 1
block = 1

# for each line, print spaces and blocks, adding a blocks and decreasing a space
for i in range(height):
    spaces = space * " "
    blocks = block * "#"
    print(spaces + blocks + "  " + blocks)
    space -= 1
    block += 1