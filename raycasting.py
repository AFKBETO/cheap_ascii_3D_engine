import math
x, y, a, n = 1635, 1440, 175, 20
grid = ['####################',
'#......#.....#..#..#',
'#......#.....#..#.##',
'#......#...........#',
'###..###.........###',
'#..................#',
'#..................#',
'#......#...........#',
'#......#.....#######',
'#............#.....#',
'#............#.###.#',
'#............#.#####',
'#............#.....#',
'#............#####.#',
'#...............0..#',
'#............#.....#',
'#............###...#',
'#............#.....#',
'#..................#',
'####################']

def main():
    h = 15
    w = 61
    results = []
    walls = [[0, ''] for i in range(w)]

    for i in range(w):
        wall, ax, ay = raycasting(x // 100, y // 100, x, y, a - (w // 2) + i)
        walls[i][1] = wall
        d = math.sqrt((ax - x)**2 + (ay - y)**2)
        dprime = d * math.cos(math.radians(- (w // 2) + i))
        height = round(1500 / dprime)
        walls[i][0] = height
        with open("output.txt", 'a') as f:
            f.write(f"{walls[i]} {ax} {ay}\n")
    
    for i in range(h + 1):
        string = []
        for j in range(w):
            string.append(' ') if (i < (h - walls[j][0])) else string.append(walls[j][1])
        results.append(''.join(string))
    for i in range(h):
        results.append(results[h - 1 - i])
    
    for i, result in enumerate(results):
        if h / 2 < i < 3 * h / 2 - 1:
            print(result)


def raycasting(xx: int, yy: int, sx: int, sy: int, angle: int):
    if angle > 180:
        angle = angle - 360
    if  angle <= -180:
        angle = angle + 360
        
    a = math.tan(math.radians(angle))
    b = sy - a * sx

    if -90 < angle < 90:
        # y = ax + b
        rx = 100 * (xx + 1)
        ry = a * rx + b
        with open("output.txt", 'a') as f:
            f.write(f"1st test {angle} {xx} {yy} {rx} {ry}\n")
        if yy * 100 <= ry <= (yy + 1) * 100:
            if grid[yy][xx + 1] == '#':
                return ',', rx, ry
            return raycasting(xx + 1, yy, sx, sy, angle)
    if 0 < angle < 180:
        ry = 100 * (yy + 1)
        rx = (ry - b) / a
        with open("output.txt", 'a') as f:
            f.write(f"2nd test {angle} {xx} {yy} {rx} {ry}\n")
        if xx * 100 <= rx <= (xx + 1) * 100:
            if grid[yy + 1][xx] == '#':
                return '.', rx, ry
            return raycasting(xx, yy + 1, sx, sy, angle)
    if angle < -90 or 90 < angle:
        rx = 100 * xx
        ry = a * rx + b
        with open("output.txt", 'a') as f:
            f.write(f"3rd test {angle} {xx} {yy} {rx} {ry}\n")
        if yy * 100 <= ry <= (yy + 1) * 100:
            if grid[yy][xx - 1] == '#':
                return ',', rx, ry
            return raycasting(xx - 1, yy, sx, sy, angle)
    if -180 < angle < 0:
        ry = 100 * yy
        rx = (ry - b) / a
        with open("output.txt", 'a') as f:
            f.write(f"4th test {angle} {xx} {yy} {rx} {ry}\n")
        if xx * 100 <= rx <= (xx + 1) * 100:
            if grid[yy - 1][xx] == '#':
                return '.', rx, ry
            return raycasting(xx, yy - 1, sx, sy, angle)

    return f"error: raycasting({xx}, {yy}, {sx}, {sy}, {angle})", rx, ry


if __name__ == "__main__":
    main()

# 1635 1440 175 20
#    01234567890123456789
# 00 ####################
# 01 #......#.....#..#..#
# 02 #......#.....#..#.##
# 03 #......#...........#
# 04 ###..###.........###
# 05 #..................#
# 06 #..................#
# 07 #......#...........#
# 08 #......#.....#######
# 09 #............#.....#
# 10 #............#.###.#
# 11 #............#.#####
# 12 #............#.....#
# 13 #............#####.#
# 14 #...............0..#
# 15 #............#.....#
# 16 #............###...#
# 17 #............#.....#
# 18 #..................#
# 19 ####################