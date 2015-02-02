class RedBlackNode(object):
  def __init__(self, key):
    self.key = key
    self.parent = None
    self.left = None
    self.right = None
    self.color = None

  def get_side(self, side):
    return getattr(self, side)

  def set_side(self, side, node):
    setattr(self, side, node)

class RedBlackTree(object):
  RED = 'red'
  BLACK = 'black'

  def __init__(self, node=None):
    self.TREE_NIL = RedBlackNode(None)
    self.TREE_NIL.color = self.BLACK
    if node != None:
      self.root = RedBlackNode(node)
    else:
      self.root = self.TREE_NIL
      self.root.left = self.TREE_NIL
      self.root.right = self.TREE_NIL

  def _create_node(self, key):
    new_node = RedBlackNode(key)
    new_node.right = self.TREE_NIL
    new_node.left = self.TREE_NIL
    new_node.color = self.RED
    return new_node

  def insert(self, key):
    new_node = self._create_node(key)
    local_parent = self.TREE_NIL
    local_root = self.root
    while local_root != self.TREE_NIL:
      local_parent = local_root
      if new_node.key < local_root.key:
        local_root = local_root.left
      else:
        local_root = local_root.right
    new_node.parent = local_parent
    if local_parent == self.TREE_NIL:
      self.root = new_node
    elif new_node.key < local_parent.key:
      local_parent.left = new_node
    else:
      local_parent.right = new_node

    self._insert_fixup(new_node)

  def _insert_fixup(self, current_node):
    def fixup(side_1, side_2, current):
      uncle = current.parent.parent.get_side(side_2)
      if uncle.color == self.RED:
        current.parent.color = self.BLACK
        uncle.color = self.BLACK
        current.parent.parent.color = self.RED
        current = current.parent.parent
      else:
        if current == current.parent.get_side(side_2):
          current = current.parent
          self._rotate(side_1, current)
        current.parent.color = self.BLACK
        current.parent.parent.color = self.RED
        self._rotate(side_2, current.parent.parent)
      return current

    while current_node.parent.color == self.RED:
      if current_node.parent == current_node.parent.parent.get_side('left'):
        current_node = fixup('left', 'right', current_node)
      else:
        current_node = fixup('right', 'left', current_node)
    self.root.color = self.BLACK

  def _rotate(self, side, start):
    def do_rotate(side_1, side_2, pivot):
      other = pivot.get_side(side_2)
      pivot.set_side(side_2, other.get_side(side_1))
      if other.get_side(side_1) != self.TREE_NIL:
        other.get_side(side_1).parent = pivot
      other.parent = pivot.parent
      if pivot.parent == self.TREE_NIL:
        self.root = other
      elif pivot == pivot.parent.get_side(side_1):
        pivot.parent.set_side(side_1, other)
      else:
        pivot.parent.set_side(side_2, other)
      other.set_side(side_1, pivot)
      pivot.parent = other

    if side == 'left':
      do_rotate('left', 'right', start)
    else:
      do_rotate('right', 'left', start)

  def _transplant(self, node_1, node_2):
    if node_1.parent == self.TREE_NIL:
      self.root = node_2
    elif node_1 == node_1.parent.left:
      node_1.parent.left = node_2
    else:
      node_1.parent.right = node_2
    node_2.parent = node_1.parent

  def delete(self, key):
    old_node = self._find_node(key)
    target_original_color = old_node.color
    target = old_node
    child_reference = None

    if old_node.left == self.TREE_NIL:
      child_reference = old_node.right
      self._transplant(old_node, old_node.right)
    elif old_node.right == self.TREE_NIL:
      child_reference = old_node.left
      self._transplant(old_node, old_node.left)
    else:
      target = self._tree_min(old_node.right)
      target_original_color = target.color
      child_reference = target.right
      if target.parent == old_node:
        child_reference.parent = target
      else:
        self._transplant(target, target.right)
        target.right = old_node.right
        target.right.parent = target
      self._transplant(old_node, target)
      target.left = old_node.left
      target.left.parent = target
      target.color = old_node.color
    if target_original_color == self.BLACK:
      self._delete_fixup(child_reference)

  def _delete_fixup(self, current_node):
    def fixup(side_1, side_2, current):
      sibling = current.parent.get_side(side_2)
      if sibling.color == self.RED:
        sibling.color = self.BLACK
        current.parent.color = self.RED
        self._rotate(side_1, current.parent)
        sibling = current.parent.get_side(side_2)
      if sibling.get_side('left').color == self.BLACK and sibling.get_side(side_2).color == self.BLACK:
        sibling.color = self.RED
        current = current.parent
      else:
        if sibling.get_side(side_2).color == self.BLACK:
          sibling.get_side(side_1).color = self.BLACK
          sibling.color = self.RED
          self._rotate(side_2, sibling)
          sibling = current.parent.get_side(side_2)
        sibling.color = current.parent.color
        current.parent.color = self.BLACK
        sibling.get_side(side_2).color = self.BLACK
        self._rotate(side_1, current.parent)
        current = self.root
      return current

    while current_node != self.root and current_node.color == self.BLACK:
      if current_node == current_node.parent.left:
        current_node = fixup('left', 'right', current_node)
      else:
        current_node = fixup('right', 'left', current_node)
    current_node.color = self.BLACK

  def _find_node(self, key):
    current_node = self.root
    while current_node != self.TREE_NIL and current_node.key != key:
      if current_node.key < key:
        current_node = current_node.right
      else:
        current_node = current_node.left
    return current_node

  def _tree_min(self, node):
    while node.left != self.TREE_NIL:
      node = node.left
    return node

  def _tree_max(self, node):
    while node.right != self.TREE_NIL:
      node = node.right
    return node

  def list(self, start_key, end_key):
    def tree_walk(low, high, node, container):
      if node != self.TREE_NIL:
        if low < node.key:
          tree_walk(low, high, node.left, container)
        if low <= node.key and high >= node.key:
          container.append(node.key)
        if high > node.key:
          tree_walk(low, high, node.right, container)

    tree = self._lowest_common_ancestor(start_key, end_key)
    results = []
    tree_walk(start_key, end_key, tree, results)
    return results

  def trouble_list(self, start_key, end_key):
    def tree_walk(low, high, node, container):
      if node != self.TREE_NIL:
        if low < node.key:
          tree_walk(low, high, node.left, container)
        if low <= node.key and high >= node.key:
          container.append([node.key, node.color, node == self.root, node == self.TREE_NIL])
        if high > node.key:
          tree_walk(low, high, node.right, container)

    tree = self._lowest_common_ancestor(start_key, end_key)
    results = []
    if tree != self.TREE_NIL:
      tree_walk(start_key, end_key, tree, results)
    return results

  def count(self, start_key, end_key):
    return len(self.list(start_key, end_key))


  def _lowest_common_ancestor(self, low, high):
    def find_ancestor(node):
      if node == self.TREE_NIL:
        return node
      elif node.key <= high and node.key >= low:
        return node
      elif node.key > high:
        return find_ancestor(node.left)
      elif node.key < low:
        return find_ancestor(node.right)

    return find_ancestor(self.root)
