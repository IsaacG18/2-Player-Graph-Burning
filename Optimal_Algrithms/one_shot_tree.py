class Node:
    def __init__(self, value=None, children=None, parent=None):
        self.value = value
        self.parent = parent
        self.children = children if children is not None else []


def tree_value(cur_node):
    cur_node.value = 1
    for child in cur_node.children:
        cur_node.value += tree_value(child)
    return cur_node.value

def find_max_root(root):
    new_root = None
    for child in root.children:
        if root.value - child.value > child.value:
            new_root = child
            break
    if new_root is None:
        return root
    root.children.remove(new_root)
    root.value -= new_root.value
    new_root.value += root.value
    new_root.children.append(root)
    return find_max_root(new_root)

    

