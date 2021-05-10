"""
File: bstnode.py
Author: Ken Lambert
"""

class BSTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

    # def __str__(self):
    #     return f'data: {self.data}; left: {self.left}; right: {self.right}'
