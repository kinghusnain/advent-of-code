# Lint as: python3
r"""Advent of Code, Day 18 -- Many-Worlds Interpretation.

>>> dopest_route_iter(graph_from_tiles('''
... ########################
... #...............b.C.D.f#
... #.######################
... #.....@.a.B.c.d.A.e.F.g#
... ########################
... '''), '@')
('@bacdfeg', 132)
>>> dopest_route_iter(graph_from_tiles('''
... ########################
... #@..............ac.GI.b#
... ###d#e#f################
... ###A#B#C################
... ###g#h#i################
... ########################
... '''), '@')
('@acfidgbeh', 81)
"""
# >>> dopest_route(graph_from_tiles('''
# ... #################
# ... #i.G..c...e..H.p#
# ... ########.########
# ... #j.A..b...f..D.o#
# ... ########@########
# ... #k.E..a...g..B.n#
# ... ########.########
# ... #l.F..d...h..C.m#
# ... #################
# ... '''), '@')
# """


import doctest
import pickle


KEY_TILES = 'abcdefghijklmnopqrstuvwxyz'
DOOR_TILES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def dopest_route(navgraph, origin, time_to_beat=None):
  """Find the dopest route.

  >>> navgraph = {
  ...     '@': {'a': 2, 'A': 2},
  ...     'a': {'@': 2},
  ...     'A': {'@': 2, 'b': 2},
  ...     'b': {'A': 2},
  ... }
  >>> dopest_route(navgraph, '@')
  ('@ab', 8)
  >>> ########################
  >>> #f.D.E.e.C.b.A.@.a.B.c.#
  >>> ######################.#
  >>> #d.....................#
  >>> ########################
  >>> navgraph = {
  ...     'f': {'D': 2},
  ...     'D': {'f': 2, 'E': 2},
  ...     'E': {'D': 2, 'e': 2},
  ...     'e': {'E': 2, 'C': 2},
  ...     'C': {'e': 2, 'b': 2},
  ...     'b': {'C': 2, 'A': 2},
  ...     'A': {'b': 2, 'a': 4},
  ...     '@': {'A': 2, 'a': 2},
  ...     'a': {'A': 4, 'B': 2},
  ...     'B': {'a': 2, 'c': 2},
  ...     'c': {'B': 2, 'd': 24},
  ...     'd': {'c': 24}
  ... }
  >>> dopest_route(navgraph, '@')
  ('@abcdef', 86)
  """
  assert origin in '@'+KEY_TILES
  if origin in KEY_TILES:
    navgraph = remove_node(navgraph, origin.upper())
  route_distances = {}
  for destination, distance in [(des, dis)
                                for des, dis in navgraph[origin].items()
                                if des in KEY_TILES]:
    if time_to_beat and time_to_beat < distance:
      pass
    else:
      route, ext_distance = dopest_route(remove_node(navgraph, origin), destination, time_to_beat=time_to_beat)
      route_distances[route] = distance + ext_distance
      if not time_to_beat or distance + ext_distance < time_to_beat:
        time_to_beat = distance + ext_distance
  if len(route_distances) == 0:
    return origin, 0
  else:
    dopest = None
    shortest_distance = None
    for route, distance in route_distances.items():
      if dopest == None:
        dopest = route
        shortest_distance = distance
      else:
        if distance < shortest_distance:
          dopest = route
          shortest_distance = distance
    return origin+dopest, shortest_distance


def dopest_route_iter(orig_graph, orig_start):
  """Find the dopest route iteratively.

  >>> navgraph = {
  ...     '@': {'a': 2, 'A': 2},
  ...     'a': {'@': 2},
  ...     'A': {'@': 2, 'b': 2},
  ...     'b': {'A': 2},
  ... }
  >>> dopest_route_iter(navgraph, '@')
  ('@ab', 8)
  >>> ########################
  >>> #f.D.E.e.C.b.A.@.a.B.c.#
  >>> ######################.#
  >>> #d.....................#
  >>> ########################
  >>> navgraph = {
  ...     'f': {'D': 2},
  ...     'D': {'f': 2, 'E': 2},
  ...     'E': {'D': 2, 'e': 2},
  ...     'e': {'E': 2, 'C': 2},
  ...     'C': {'e': 2, 'b': 2},
  ...     'b': {'C': 2, 'A': 2},
  ...     'A': {'b': 2, 'a': 4},
  ...     '@': {'A': 2, 'a': 2},
  ...     'a': {'A': 4, 'B': 2},
  ...     'B': {'a': 2, 'c': 2},
  ...     'c': {'B': 2, 'd': 24},
  ...     'd': {'c': 24}
  ... }
  >>> dopest_route_iter(navgraph, '@')
  ('@abcdef', 86)
  """
  dopest_routes = {}
  paths_to_investigate = []
  paths_to_investigate.append((orig_graph, orig_start))

  while paths_to_investigate:
    navgraph, origin = paths_to_investigate.pop()
    navgraph_copy = {k: v.copy() for (k, v) in navgraph.items()}
    assert origin in '@'+KEY_TILES
    if origin in KEY_TILES:
      navgraph = remove_node(navgraph, origin.upper())
    navgraph_without_origin = remove_node(navgraph, origin)

    # If I have scores for all reachable keys, dopest route is smallest of
    # (dist_to_key + key_score)
    have_scores = True
    reachable_keys = [k for k in navgraph[origin].keys() if k in KEY_TILES]
    for k in reachable_keys:
      if pickle.dumps((navgraph_without_origin, k)) not in dopest_routes:
        have_scores = False
    if have_scores:
      dopest = None
      shortest_distance = None
      for k in reachable_keys:
        route, ext_distance = dopest_routes[pickle.dumps((navgraph_without_origin, k))]
        distance = ext_distance + navgraph[origin][k]
        if dopest == None:
          dopest = route
          shortest_distance = distance
        else:
          if distance < shortest_distance:
            dopest = route
            shortest_distance = distance
      if dopest == None:
        dopest_routes[pickle.dumps((navgraph_copy, origin))] = (origin, 0)
      else:
        dopest_routes[pickle.dumps((navgraph_copy, origin))] = (origin+dopest, shortest_distance)

    # Else, push unknown scores onto paths_to_investigate
    else:
      paths_to_investigate.append((navgraph_copy, origin))
      for destination, distance in [(des, dis)
                                    for des, dis in navgraph[origin].items()
                                    if des in KEY_TILES]:
        paths_to_investigate.append((navgraph_without_origin, destination))

  return dopest_routes[pickle.dumps((orig_graph, orig_start))]


def remove_node(navgraph, node):
  """Remove a node from the graph, rewriting edges.

  >>> navgraph = {
  ...     '@': {'a': 2, 'A': 2},
  ...     'a': {'@': 2},
  ...     'A': {'@': 2, 'b': 2},
  ...     'b': {'A': 2},
  ... }
  >>> remove_node(navgraph, 'A')
  {'@': {'a': 2, 'b': 4}, 'a': {'@': 2}, 'b': {'@': 4}}
  """
  new_graph = {}
  for landmark, exits in [(l, e) for l, e in navgraph.items() if l != node]:
    new_exits = {}
    for destination, distance in exits.items():
      if destination == node:
        for far_dest, far_dist in [(de, di)
                                   for de, di in navgraph[destination].items()
                                   if de != landmark]:
          if far_dest not in navgraph[landmark]:
            new_exits[far_dest] = distance + far_dist
          else:
            new_exits[far_dest] = navgraph[landmark][far_dest]
      else:
        new_exits[destination] = distance
    new_graph[landmark] = new_exits
  return new_graph


def graph_from_tiles(tiles):
  """
  >>> graph_from_tiles('''
  ... #########
  ... #b.A.@.a#
  ... #########
  ... ''')
  {'b': {'A': 2}, 'A': {'b': 2, 'a': 4}, '@': {'A': 2, 'a': 2}, 'a': {'A': 4}}
  >>> graph_from_tiles('''
  ... ########################
  ... #@..............ac.GI.b#
  ... ###d#e#f################
  ... ###A#B#C################
  ... ###g#h#i################
  ... ########################
  ... ''')
  {'@': {'d': 3, 'e': 5, 'f': 7, 'a': 15}, 'a': {'c': 1, 'f': 10, 'e': 12, 'd': 14}, 'c': {'a': 1, 'G': 2}, 'G': {'I': 1, 'c': 2}, 'I': {'G': 1, 'b': 2}, 'b': {'I': 2}, 'd': {'A': 1, 'e': 4, 'f': 6, 'a': 14}, 'e': {'B': 1, 'd': 4, 'f': 4, 'a': 12}, 'f': {'C': 1, 'e': 4, 'd': 6, 'a': 10}, 'A': {'d': 1, 'g': 1}, 'B': {'e': 1, 'h': 1}, 'C': {'f': 1, 'i': 1}, 'g': {'A': 1}, 'h': {'B': 1}, 'i': {'C': 1}}
  """
  tile_grid = tiles.strip().split('\n')
  grid_height = len(tile_grid)
  grid_width = len(tile_grid[0])
  graph = {}
  for y in range(grid_height):
    for x in range(grid_width):
      tile = tile_grid[y][x]
      if tile in '@'+KEY_TILES+DOOR_TILES:
        graph[tile] = exits_from_landmark(tile_grid, (x, y))
  return graph


def exits_from_landmark(tile_map, origin):
  """

  >>> exits_from_landmark([
  ...     '#########',
  ...     '#b.A.@.a#',
  ...     '#########'], (1, 1))
  {'A': 2}
  >>> exits_from_landmark([
  ...     '#########',
  ...     '#b.A.@.a#',
  ...     '#########'], (3, 1))
  {'b': 2, 'a': 4}
  >>> exits_from_landmark([
  ...     '#########',
  ...     '#b.A.@.a#',
  ...     '#########'], (5, 1))
  {'A': 2, 'a': 2}
  """
  space_tiles = '.@'
  h, w = len(tile_map), len(tile_map[0])
  orig_x, orig_y = origin
  tile = tile_map[orig_y][orig_x]
  reachablity_map = [[False for _ in row] for row in tile_map]
  reachablity_map[orig_y][orig_x] = True
  done = False
  steps = 0
  exits = {}
  while not done:
    map_iter = [[val for val in row] for row in reachablity_map]
    steps += 1
    for y in range(h):
      for x in range(w):
        if reachablity_map[y][x]:
          north_tile = tile_map[y - 1][x] if y - 1 >= 0 else '??'
          south_tile = tile_map[y + 1][x] if y + 1 < h else '??'
          west_tile = tile_map[y][x - 1] if x - 1 >= 0 else '??'
          east_tile = tile_map[y][x + 1] if x + 1 < w else '??'

          # Add adjacent keys and doors to `exits`.
          for t in [north_tile, south_tile, west_tile, east_tile]:
            if t in KEY_TILES+DOOR_TILES and t not in exits and t != tile:
              exits[t] = steps

          # Mark adjacent spaces as reachable.
          if north_tile in space_tiles:
            map_iter[y - 1][x] = True
          if south_tile in space_tiles:
            map_iter[y + 1][x] = True
          if west_tile in space_tiles:
            map_iter[y][x - 1] = True
          if east_tile in space_tiles:
            map_iter[y][x + 1] = True
    done = map_iter == reachablity_map
    reachablity_map = [[val for val in row] for row in map_iter]
  return exits


def solve_pt1():
  with open('advent18_tunnels.txt') as f:
    tunnels = f.read()
  print('Building navigation graph...', end='', flush=True)
  navgraph = graph_from_tiles(tunnels)
  print('done.', flush=True)

  print('Finding dopest route...', end='', flush=True)
  _, steps = dopest_route_iter(navgraph, '@')
  print('done. {} steps.'.format(steps))


def solve_pt2():
  pass


if __name__ == '__main__':
  doctest.testmod()
  solve_pt1()
  #solve_pt2()
