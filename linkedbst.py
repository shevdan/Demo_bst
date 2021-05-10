"""
Implementation of the linked binary tree
"""

from math import log
from time import time
import random
import sys
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

sys.setrecursionlimit(10**6)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            text = ""
            if node is not None:
                text += recurse(node.right, level + 1)
                text += "| " * level
                text += str(node.data) + "\n"
                text += recurse(node.left, level + 1)
            return text

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def __len__(self):
        return self._size

    # def preorder(self):
    #     """Supports a preorder traversal on a view of self."""
    #     return

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    # def postorder(self):
    #     """Supports a postorder traversal on a view of self."""
    #     return None

    # def levelorder(self):
    #     """Supports a levelorder traversal on a view of self."""
    #     return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)
            return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return

    def is_leaf(self, pos):
        '''
        Return if a node is a leaf
        '''
        return pos.left is None and pos.right is None

    def children(self, position):
        '''
        Yields node's left and right children
        '''
        if position.left is not None:
            yield position.left
        if position.right is not None:
            yield position.right


    def height(self, p=None):
        '''
        Return the height of tree
        :return: int
        '''
        def _height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self.is_leaf(top):
                return 0
            return 1 + max(_height1(c) for c in self.children(top))

        if p is None:
            p = self._root
        return _height1(p)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(len(self), 2)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        item_lst = []

        def recurse(node, low, high):
            if node is not None:
                recurse(node.left, low, high)
                if low <= node.data <= high:
                    item_lst.append(node.data)
                recurse(node.right, low, high)

        recurse(self._root, low, high)
        return item_lst


    def rebalance(self):
        '''
        Rebalances the tree.
        '''
        tree_items = sorted([item for item in self.inorder()])
        self.clear()
        # mid = (len(tree_items) // 2) + 1
        # mid_el = tree_items[mid]
        # left_lst = tree_items[:mid]
        # right_lst = tree_items[(mid + 1):]

        balanced_items = []
        def recurse(tree_items):
            if not tree_items:
                return
            mid = (len(tree_items) // 2)
            balanced_items.append(tree_items[mid])

            recurse(tree_items[:mid])
            recurse(tree_items[(mid + 1):])

        recurse(tree_items)

        for elm in balanced_items:
            self.add(elm)

        return tree_items

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """
        def recurse(node, item):
            if node is None:
                return
            if node.data > item and (node.left is None or self.maximum(node.left) <= item):
                return node.data
            if node.data <= item:
                return recurse(node.right, item)
            if node.data > item:
                return recurse(node.left, item)

        return recurse(self._root, item)

    def minimum(self, node):
        '''
        Returns the minimum node of the tree
        '''
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr.data

    def maximum(self, node):
        '''
        Return the maximum node of the tree
        '''
        curr = node
        while curr.right is not None:
            curr = curr.right
        return curr.data


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """
        def recurse(node, item):
            if node is None:
                return
            if node.data < item and (node.right is None or self.minimum(node.right) >= item):
                return node.data
            if node.data >= item:
                return recurse(node.left, item)
            if node.data < item:
                return recurse(node.right, item)

        return recurse(self._root, item)


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        def parse_words(path):
            words = []
            with open(path) as file:
                for line in file:
                    words.append(line.strip())
            return words
        
        def check_lst_sorted(words):
            now = time()
            for _ in range(10000):
                word = random.choice(words)
                words.index(word)
            program_time = time() - now
            return program_time

        def check_bst_sorted(words):
            bst = LinkedBST()
            for word in words:
                bst.add(word)

            now = time()
            for _ in range(10000):
                word = random.choice(word)
                bst.find(word)
            program_time = time() - now
            bst.clear()
            return program_time
        
        def check_bst_random(words):
            bst = LinkedBST()
            random.shuffle(words)
            for word in words:
                bst.add(word)
            
            now = time()
            for _ in range(10000):
                word = random.choice(word)
                bst.find(word)
            program_time = time() - now
            bst.clear()
            return program_time

        def check_bst_balanced(words):
            bst = LinkedBST()
            random.shuffle(words)
            for word in words:
                bst.add(word)
            bst.rebalance()
            
            now = time()
            for _ in range(10000):
                word = random.choice(word)
                bst.find(word)
            program_time = time() - now
            bst.clear()
            return program_time

        words = parse_words(path)[:10000]
        print(f'Program takes {round(check_lst_sorted(words), 3)} seconds to find 10000 occurences of random \
words in a sorted list of 10k words')

        print(f'Program takes {round(check_bst_sorted(words), 3)} seconds to find 10000 occurences of random \
words in a bst constructed on a sorted list of 10k words')

        print(f'Program takes {round(check_bst_random(words), 3)} seconds to find 10000 occurences of random \
words in a bst constructed on a random list of 10k words')

        print(f'Program takes {round(check_bst_balanced(words), 3)} seconds to find 10000 occurences of random \
words in a balanced bst constructed on a random list of 10k words')



if __name__ == '__main__':
    
    a = LinkedBST()
    path = '/Users/shevdan/Documents/Programming/Python/semester2/lab13/binary_search_tree/words.txt'
    a.demo_bst(path)