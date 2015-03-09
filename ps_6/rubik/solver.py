import rubik

def apply_permutations(node, parents):
  def permute(permutation):
    return rubik.perm_apply(permutation, node)

  descendents = []
  for p in rubik.quarter_twists:
    next_node = permute(p)
    if not parents.has_key(next_node):
      parents[next_node] = (node, p)
      descendents.append(next_node)
  return (descendents, parents)

def perm_identity(perm):
  return perm

def build_path(state, start_parents, end_parents):
  def increment_path(parents, node, current_path, perm_direction):
    next_step = parents.get(node)
    path.append(perm_direction(next_step[1]))
    return (next_step[0], path)

  path = []
  next_state = state
  while start_parents.get(next_state) is not None:
    next_state, path = increment_path(start_parents, next_state, path,
        perm_identity)

  path.reverse()

  next_state = state
  while end_parents.get(next_state) is not None:
    next_state, path = increment_path(end_parents, next_state, path,
        rubik.perm_inverse)

  return path

def iterations_to_max_depth():
  number_of_permutations = len(rubik.quarter_twists)
  max_depth_of_rubiks_cube = 14
  return number_of_permutations ** ((max_depth_of_rubiks_cube - 1) / 2)

def shortest_path(start, end):
  """
  Using 2-way BFS, finds the shortest path from start_position to
  end_position. Returns a list of moves.

  You can use the rubik.quarter_twists move set.
  Each move can be applied using rubik.perm_apply
  """
  iter_count = 0
  max_iter = iterations_to_max_depth()
  start_parents  = { start: None }
  end_parents = { end: None }
  start_queue = [start]
  end_queue = [end]
  while len(start_queue) > 0 and len(end_queue) > 0:
    start = start_queue.pop(0)
    end = end_queue.pop(0)
    if end_parents.has_key(start):
      return build_path(start, start_parents, end_parents)
    elif start_parents.has_key(end):
      return build_path(end, start_parents, end_parents)
    elif iter_count > max_iter:
      return None
    else:
      start_descendents, start_parents = apply_permutations(start, start_parents)
      end_descendents, end_parents = apply_permutations(end, end_parents)
      [start_queue.append(node) for node in start_descendents]
      [end_queue.append(node) for node in end_descendents]
      iter_count += 1
