from collections import defaultdict
import math
import functools
import time

# Inputs
# x, y  : coordinates of the camera
# a     : camera angle
# n     : map size in number of tiles
x, y, an, n = 1200, 910, 120, 20

# the map
# # marks wall
# . marks open space
# camera's coordinates must be in open space
map = [
    '####################', # 00
    '#......#.....#..#..#', # 01
    '#......#.....#..#.##', # 02
    '#......#...........#', # 03
    '###..###.........###', # 04
    '#..................#', # 05
    '#..................#', # 06
    '#......#...........#', # 07
    '#......#.....#######', # 08
    '#......#.....#.....#', # 09
    '#......#...0.#.###.#', # 10
    '#...######.###.#####', # 11
    '#.....#......#.....#', # 12
    '#.....#......#####.#', # 13
    '#..................#', # 14
    '#............#.....#', # 15
    '#............###...#', # 16
    '#............#.....#', # 17
    '#..................#', # 18
    '####################'  # 19
]   #0    5    0    5   9

# timer function, used with decorator for main() function
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        string = f"Finished {func.__name__!r} in {run_time:.4f} secs"
        
        # output into file
        with open("output.txt", 'a') as f:
            f.write(string)
        print(string)
        return value
    return wrapper_timer

@timer
def main():
    # picture size (w x h). Change these values to change the resolution
    w, h = 61, 15
    
    # reset the output file
    with open("output.txt", 'w') as f:
        f.write(f"{x} {y} {an} {n}\n")
    
    # results is the array of ASCII string
    for a in range(an - 30, an + 30, 2):
        results = []
        # walls contain the height and the type of wall, based on the column
        walls = [[0, ''] for i in range(w)]

        # calculation of the wall height and wall type
        for i in range(w):
            wall, ax, ay = raycasting(x // 100, y // 100, x, y, a - (w // 2) + i)

            walls[i][1] = wall

            d = math.sqrt((ax - x)**2 + (ay - y)**2)
            dprime = d * math.cos(math.radians(- (w // 2) + i))
            height = round(h * 100 / dprime)
            walls[i][0] = height

            with open("output.txt", 'a') as f:
                f.write(f"{walls[i]} {ax} {ay}\n")
        
        # construction of the upper half of the image.
        # we only have to construct the upper half since the image is symetric
        # the loop ends at h // 2 + 1 to construct the middle row
        for i in range(h // 2 + 1):
            string = []
            for j in range(w):
                # check height
                # + h//2 to only take the central part of the rows of the image
                string.append(' ') if (i + h // 2 + 1 < (h - walls[j][0])) else string.append(walls[j][1])
            results.append(''.join(string))
        
        # copy and flip the upper half of the image
        for i in range(h // 2):
            results.append(results[h // 2 - 1 - i])
        
        # print the result
        for i, result in enumerate(results):
            print(result)
        print('\n')

# This function is used to find the intersection of a ray casted from an
# origin to a wall. This function will search recursively through the gridmap 
# until when it finds a wall
# @param:
# xx    (int): the column number of the current grid
# yy    (int): the row number of the current grid
# sx  (float): x-coordinate of the origin (can be outside of current grid)
# sy  (float): y-coordinate of the origin (can be outside of current grid)
# angle (int): angle of the camera
# @return:
# str        : the type of wall that the ray intersects with. '.' for a h-wall
#              or ',' for a v-wall
# float      : x-coordinate of the intersection
# float      : y-coordinate of the intersection
# @error:
# str        : error message (in the form of the function called)
# rx, ry     : final coordinates that got the error
def raycasting(xx: int, yy: int, sx: int, sy: int, angle: int) -> tuple[str, float, float]:

    # reconvert the angle to a number a so that - 180 < a <= 180
    if angle > 180:
        angle = angle - 360
    if  angle <= -180:
        angle = angle + 360
    
    # calculation of all coefficients of the function of a line based on its 
    # angle and a known point on the line (here is the origin)
    # Remark: function of a line is y = ax + b
    a = math.tan(math.radians(angle))
    b = sy - a * sx
    
    # xx          xx + 1
    # A_____________B yy
    # |             |
    # |             |
    # |             |
    # |             |
    # |             |
    # |_____________| yy + 1
    # D             C
    
    # check if the angle hits BC segment or not (angle between -90 and 90)
    if -90 < angle < 90:
        # calculation of the intersection with the line going through B and 
        # C, this line's function is actually x = 100 * (xx + 1)
        rx = 100 * (xx + 1)
        ry = round(a * rx + b, 7)

        with open("output.txt", 'a') as f:
            f.write(f"1st test {angle} {xx} {yy} {rx} {ry}\n")
        
        # check if (rx, ry) is on BC segment (not just on the line); if not, 
        # ignore and start the next check
        if yy * 100 <= ry <= (yy + 1) * 100:
            # check if we hit a wall
            if map[yy][xx + 1] == '#':
                return ',', rx, ry
            # if we haven't hit a wall yet, do the same calculation with the 
            # next tile
            return raycasting(xx + 1, yy, sx, sy, angle)
    
    # check if the angle hits CD segment or not (angle between 0 and 180)
    if 0 < angle < 180:
        ry = 100 * (yy + 1)
        rx = round((ry - b) / a, 7)
        with open("output.txt", 'a') as f:
            f.write(f"2nd test {angle} {xx} {yy} {rx} {ry}\n")
        if xx * 100 <= rx <= (xx + 1) * 100:
            if map[yy + 1][xx] == '#':
                return '.', rx, ry
            return raycasting(xx, yy + 1, sx, sy, angle)
    
    # check if the angle hits AD segment or not (angle < -90 or angle > 90)
    if angle < -90 or 90 < angle:
        rx = 100 * xx
        ry = round(a * rx + b, 7)
        with open("output.txt", 'a') as f:
            f.write(f"3rd test {angle} {xx} {yy} {rx} {ry}\n")
        if yy * 100 <= ry <= (yy + 1) * 100:
            if map[yy][xx - 1] == '#':
                return ',', rx, ry
            return raycasting(xx - 1, yy, sx, sy, angle)
    
    # check if the angle hits AB segment or not (angle between -180 and 0)
    if -180 < angle < 0:
        ry = 100 * yy
        rx = round((ry - b) / a, 7)
        with open("output.txt", 'a') as f:
            f.write(f"4th test {angle} {xx} {yy} {rx} {ry}\n")
        if xx * 100 <= rx <= (xx + 1) * 100:
            if map[yy - 1][xx] == '#':
                return '.', rx, ry
            return raycasting(xx, yy - 1, sx, sy, angle)
    
    # return errors should it meets any error
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

