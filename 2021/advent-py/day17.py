from typing import Generator, Tuple, Dict


def is_hit(x_veloc: int, y_veloc: int, t: int,
           x_lower: int, x_upper: int,
           y_lower: int, y_upper: int) -> bool:
    '''Returns True if starting velocity results in a hit at time t.
    
    # >>> is_hit(7, 2, 7, 20, 30, -10, -5)
    # True
    >>> is_hit(6, 3, 9, 20, 30, -10, -5)
    True
    >>> is_hit(9, 0, 4, 20, 30, -10, -5)
    True
    '''
    # xv = 5
    # t = 0: x = 0              tri(5) - tri(5)
    # t = 1: x = 0 + 5          tri(5) - tri(5-1)
    # t = 2: x = 0 + 5 + 4      tri(5) - tri(5-2)
    # t = 3: x = 0 + 5 + 4 + 3  tri(5) - tri(5-3)
    #
    # yv = 2
    # t = 0: y = 0
    # t = 1: y = 0 + 2
    # t = 2: y = 0 + 2 + 1
    # t = 3: y = 0 + 2 + 1 + 0
    # t = 4: y = 0 + 2 + 1 + 0 - 1
    final_x = triangle(abs(x_veloc)) - triangle(abs(x_veloc) - t)
    final_y = triangle(y_veloc, -1000) - triangle(y_veloc - t, -1000)
    return (x_lower <= final_x <= x_upper) and (y_lower <= final_y <= y_upper)


def elevation(x_veloc: int, y_veloc: int, t: int,
              x_lower: int, x_upper: int,
              y_lower: int, y_upper: int) -> int:
    final_y = triangle(y_veloc, -1000) - triangle(y_veloc - t, -1000)
    return final_y


all_known_triangles: Dict[Tuple[int, int], int] = {}

def triangle(n: int, bottom: int = 0) -> int:
    '''Triangle function.
    
    >>> triangle(0)
    0
    >>> triangle(3)
    6
    >>> triangle(-1, bottom=-3)
    -6
    '''
    if (n, bottom) in all_known_triangles:
        return all_known_triangles[(n, bottom)]

    triangle = 0
    for i in range(n, bottom - 1, -1):
        triangle += i
    all_known_triangles[(n, bottom)] = triangle
    return triangle


def hits(x_lower: int, x_upper: int,
         y_lower: int, y_upper: int) -> Generator[Tuple[Tuple[int, int], int], None, None]:
    # Bounds: https://www.reddit.com/r/adventofcode/comments/rier96/2021_day_17_spoilers_best_bounds/
    for x in range(0, x_upper + 1):
        for y in range(y_lower, max(abs(y_lower), abs(y_upper)) + 1):
            apex = 0
            t = 1
            while True:
                elev = elevation(x, y, t, x_lower, x_upper, y_lower, y_upper)
                apex = elev if elev > apex else apex
                if elev < y_lower:
                    break
                if is_hit(x, y, t, x_lower, x_upper, y_lower, y_upper):
                    yield ((x, y), apex)
                t += 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # target area: x=20..30, y=-10..-5
    results = list(hits(20, 30, -10, -5))
    print(max([apex for (_, _), apex in results]))
    print(len(set([v for v, _ in results])))

    # target area: x=135..155, y=-102..-78
    results = list(hits(135, 155, -102, -78))
    print(max([apex for (_, _), apex in results]))
    print(len(set([v for v, _ in results])))
