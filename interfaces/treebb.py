from collections import deque
from math import ceil

import graphviz


class BPlusTreeNode:
    def __init__(self, is_leaf=True):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.parent = None


class BPlusTree:
    def __init__(self, order):
        self.root = BPlusTreeNode()
        self.order = order

    def insert(self, val):
        if not self.root.keys:
            # Si la racine est vide
            self.root.keys.append(val)
        else:
            # Sinon, insérer dans les sous-arbres
            self.insert_non_full(self.root, val)

    def insert_non_full(self, node, val):
        index = 0
        while index < len(node.keys) and val > node.keys[index]:
            index += 1

        # Si node est un leaf
        if node.is_leaf:
            node.keys.insert(index, val)
            if len(node.keys) == self.order:
                self.split_leaf(node)
        else:
            child = node.children[index]
            if len(child.keys) == self.order:
                self.split_non_leaf(node, index)
                if val > node.keys[index]:
                    child = node.children[index + 1]
            self.insert_non_full(child, val)

    def split_leaf(self, node):
        mid_index = self.order // 2
        left_node = BPlusTreeNode(is_leaf=True)
        right_node = BPlusTreeNode(is_leaf=True)
        left_node.keys = node.keys[:mid_index]
        right_node.keys = node.keys[mid_index:]
        # Update parent node
        parent_node = node.parent

        if parent_node is None:
            # If there is no parent (splitting root)
            new_parent = BPlusTreeNode(is_leaf=False)
            new_parent.keys = [right_node.keys[0]]  # Use the first key of the right node as the new key
            new_parent.children = [left_node, right_node]
            left_node.parent = new_parent
            right_node.parent = new_parent
            self.root = new_parent
        else:
            # If there is a parent
            index = parent_node.children.index(node)
            parent_node.keys.insert(index, right_node.keys[0])  # Use the first key of the right node as the new key
            parent_node.children.insert(index + 1, right_node)
            right_node.parent = parent_node
            left_node.parent = parent_node

        node.keys = left_node.keys
        node.children = [left_node, right_node]
        left_node.parent = node

        if parent_node and len(parent_node.keys) == self.order:
            # If the parent is full, recursively split it
            parent_index = parent_node.children.index(node)
            self.split_non_leaf(parent_node, parent_index)

    def split_non_leaf(self, parent_node, index):
        mid_index = self.order // 2

        left_node = BPlusTreeNode(is_leaf=False)
        right_node = BPlusTreeNode(is_leaf=False)

        left_node.keys = parent_node.keys[:mid_index]
        right_node.keys = parent_node.keys[mid_index + 1:]

        left_node.children = parent_node.children[:mid_index + 1]
        right_node.children = parent_node.children[mid_index + 1:]
        grandparrent_node = parent_node.parent

        if grandparrent_node is None:
            new_grandparent = BPlusTreeNode(is_leaf=False)
            new_grandparent.keys = [parent_node.keys[mid_index]]
            new_grandparent.children = [left_node, right_node]
            left_node.parent = new_grandparent
            right_node.parent = new_grandparent
            self.root = new_grandparent
        else:
            # If there is a grandparent
            grandparent_index = grandparrent_node.children.index(parent_node)
            grandparrent_node.keys.insert(grandparent_index, parent_node.keys[mid_index])
            grandparrent_node.children[grandparent_index] = left_node
            grandparrent_node.children.insert(grandparent_index + 1, right_node)
            right_node.parent = grandparrent_node
            left_node.parent = grandparrent_node

        # Mise à jour des parents de left and right childs
        for child in left_node.children:
            child.parent = left_node

        for child in right_node.children:
            child.parent = right_node

        if grandparrent_node and len(grandparrent_node.keys) == self.order:
            # If the grandparent is full, recursively split it
            self.split_non_leaf(grandparrent_node, grandparent_index)

    def delete(self, val):
        if not self.root.keys:
            # Tree is empty
            print("aa")
            return

        # Start deletion from the root
        self.delete_recursive(self.root, val)

    def find_smallest_key(self, node):
        # Helper function to find the smallest key in a subtree
        while node.is_leaf != True:
            if node.children[0].is_leaf != True:
                node = node.children[0]
            else:
                return node.keys[0]
        return node.keys[0]

    def delete_recursive(self, node, val):
        index = 0

        while index < len(node.keys) and val >= node.keys[index]:
            index += 1

        if node.is_leaf:
            # If the value is in a leaf node, delete it
            if val in node.keys:
                node.keys.remove(val)
                if val == node.parent.keys[-1]:
                    node.parent.keys.remove(val)

            else:
                print(f"Value {val} not found in the tree.")
        else:
            if val in node.keys:
                # Remplacez la valeur par la plus grande valeur du sous-arbre droite
                index_val = node.keys.index(val)
                right_subtree = node.children[index_val + 1]
                smallest_key = self.find_smallest_key(right_subtree)
                node.keys[index_val] = smallest_key
                # Continuez la suppression dans le sous-arbre droite

                # Continuez la suppression dans le sous-arbre approprié
            self.delete_recursive(node.children[index], val)


        # After deletion, check for underflow
        if len(node.keys) < (ceil(self.order / 2) - 1):
            self.handle_underflow(node)

    def handle_underflow(self, node):
        # Borrow from or merge with siblings
        parent = node.parent
        if parent is None:
            # Node is the root
            if not node.keys and len(node.children) == 1:
                self.root = node.children[0]
                self.root.parent = None

        else:
            # Node is not the root
            index = parent.children.index(node) if node in parent.children else -1

            if index > 0 and len(parent.children[index - 1].keys) > (self.order // 2):
                # Borrow from the left sibling
                self.borrow_from_left(node, index)
            elif index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > (self.order // 2):
                # Borrow from the right sibling
                self.borrow_from_right(node, index)
            elif index > 0:
                # Merge with the left sibling
                self.merge_with_left(node, index)
            else:
                # Merge with the right sibling
                self.merge_with_right(node, index)


    def borrow_from_left(self, node, index):
        # Borrow a key from the left sibling
        parent = node.parent
        if index > 0:
            left_sibling = parent.children[index - 1]
            #borrowed_child = left_sibling.children.pop()
            borrowed_key = left_sibling.keys.pop()

            node.keys.insert(0, borrowed_key)
            #node.children.insert(0, borrowed_child)

            parent.keys.append(node.keys[0])
        else:
            # If there is no left sibling, update parent's keys without borrowing
            parent.keys[index] = node.keys[0]
        if len(node.parent.keys) < (ceil(self.order / 2) - 1):
            self.handle_underflow(node.parent)

    def borrow_from_right(self, node, index):
        # Borrow a key from the right sibling
        parent = node.parent
        if len(parent.keys) < self.order // 2:
            right_sibling = parent.children[index + 1]
            borrowed_key = right_sibling.keys.pop(0)
            borrowed_child = right_sibling.children.pop(0)
            node.keys.append(borrowed_key)
            node.children.append(borrowed_child)

            parent.keys[index] = right_sibling.keys[0]
        else:
            # If the parent has enough keys, borrow the first key from the parent
            # Get first element from right sibling and delete their child
            first_element_from_left = parent.children[index + 1].keys.pop(0)
            child_of_left_sibling = parent.children[index+1].children.pop(0)
            # Get the last element of parent
            borrowed_key = parent.keys.pop(-1)
            parent.keys.append(first_element_from_left)
            #borrowed_child = parent.children.pop(-1)
            node.keys.insert(0, borrowed_key)
            #node.children.append(child_of_left_sibling)
            child_of_left_sibling.parent = node
            node.children.insert(index+1, child_of_left_sibling)



    def merge_with_left(self, node, index):
        # Merge with the left sibling

        parent = node.parent
        left_sibling = parent.children[index - 1]
        if len(parent.keys) == 0:
            merged_keys = left_sibling.keys + node.keys
        else:
            merged_keys = left_sibling.keys + [parent.keys.pop(index - 1)] + node.keys

        merged_children = left_sibling.children + node.children
        left_sibling.keys = merged_keys
        left_sibling.children = merged_children

        left_sibling.parent = node.parent.parent.children[len(node.parent.parent.keys) - 1] if node.parent.parent  else left_sibling.parent
        parent.children.pop(index)
        #left_sibling.parent = parent.parent if len(parent.keys) == 0 else parent
        node.children.clear()

        #Probleme here when deleting 11
        node.parent = None
        del node

        if len(left_sibling.parent.keys) < (ceil(self.order / 2) - 1):
            self.handle_underflow(left_sibling.parent)

    def merge_with_right(self, node, index):

        parent = node.parent
        if node.is_leaf == True:
            # Merge with the right sibling
            right_sibling = parent.children[index + 1]

            merged_keys = node.keys + right_sibling.keys
            merged_children = node.children + right_sibling.children

            # Update the keys and children of the right sibling
            right_sibling.keys = merged_keys
            right_sibling.children = merged_children

            # Remove the merged node
            right_sibling.parent.children.pop(index)
            # S'il y a une erreur j'ai fait une modification ici
            right_sibling.parent = parent
            #right_sibling.parent = node.parent.parent.children[len(node.parent.parent.keys) - 1]

            parent.keys.pop(index)

            del node

        else:
            parent_key = parent.keys.pop(-1)
            right_sibling = parent.children[index + 1]

            node.keys.append(parent_key)

            merged_keys = node.keys + right_sibling.keys
            merged_children = node.children + right_sibling.children

            right_sibling.keys = merged_keys
            right_sibling.children = merged_children
            parent.children.pop(index)

            # Update parent references of the children of the node
            for child in node.children:
                child.parent = right_sibling

            node.parent = None
            node.children.clear()
            del node


        if len(parent.keys) < (ceil(self.order / 2) - 1):
            self.handle_underflow(parent)


    def display(self):
        if not self.root.keys:
            print("The tree is empty.")
            return

        queue = deque([self.root])

        while queue:
            current_level = []
            next_level = []

            while queue:
                node = queue.popleft()
                current_level.append(node.keys)

                if not node.is_leaf:
                    next_level.extend(node.children)

            for keys in current_level:
                print(" ", end="")
                print("[", end=" ")
                print(" ".join(map(str, keys)), end=" ")
                print("]", end="")

            print("\n")

            queue.extend(next_level)

    def to_dot(self):
        dot = graphviz.Digraph()

        if not self.root.keys:
            dot.node("empty", label="L'arbre est vide.")
            return dot

        queue = deque([self.root])

        # Dictionary to store node positions at each level
        level_positions = {}

        while queue:
            current_level = []
            next_level = []

            while queue:
                node = queue.popleft()
                node_id = str(id(node))

                # Add node to the current level
                current_level.append((node_id, node))

                if not node.is_leaf:
                    for child in node.children:
                        child_id = str(id(child))
                        dot.edge(node_id, child_id)
                        next_level.append(child)

            # Store node positions for the current level
            level_positions[len(level_positions)] = current_level

            queue.extend(next_level)

        # Organize nodes horizontally by level
        for level, nodes in level_positions.items():
            with dot.subgraph() as subgraph:
                subgraph.attr(rank='same')  # Set the same rank for all nodes in the subgraph
                for i, (node_id, node) in enumerate(nodes):
                    if node.is_leaf:
                        # Set label for leaf nodes
                        leaf_label = ", ".join(map(str, node.keys))
                        if i == 0:  # Check if it's the first node
                            subgraph.node(node_id, label=leaf_label, shape='box', width='0.1')
                        else:
                            subgraph.node(node_id, label=leaf_label, shape='box')
                    else:
                        # Set label for internal nodes
                        internal_label = ", ".join(map(str, node.keys))
                        subgraph.node(node_id, label=internal_label)

        # Connect adjacent leaf nodes horizontally with arrows
        for nodes in level_positions.values():
            leaf_nodes = [node_id for node_id, node in nodes if node.is_leaf]
            for i in range(len(leaf_nodes) - 1):
                dot.edge(leaf_nodes[i], leaf_nodes[i + 1], dir='both', arrowhead='vee')

        return dot

