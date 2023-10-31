import os
import time

class RBNode:
    RED = 0
    BLACK = 1
    
    def __init__(self, key, value, color=RED, left=None, right=None, parent=None):
        '''
        Initialize a Red-Black tree node.
        
        Parameters:
            - key: the key of the node, English word (string) in this case.
            - value: the value of the node, Chinese translation (string) of the English word.
            - color: node color, RED or BLACK, default is RED.
            - left: the left child of the node, default is None.
            - right: the right child of the node, default is None.
            - parent: the parent of the node, default is None.
        '''
        self.key = key
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent
        
    def is_red(self):
        '''
        Check if the node is red.
        
        Returns:
            - True if the node is red, False otherwise.
        '''
        return self.color == RBNode.RED
    
    def is_black(self):
        '''
        Check if the node is black.
        
        Returns:
            - True if the node is black, False otherwise.
        '''
        return self.color == RBNode.BLACK
    
    def set_red(self):
        '''
        Set the node color to red.
        '''
        self.color = RBNode.RED
        
    def set_black(self):
        '''
        Set the node color to black.
        '''
        self.color = RBNode.BLACK
        
    def __str__(self):
        '''
        Return string representation of the node.
        '''
        color = "RED" if self.is_red() else "BLACK"
        return str(self.key) + ':' + str(self.value) + color

class RedBlackTree:
    def __init__(self):
        self.nil = RBNode(None, None, RBNode.BLACK)
        self.root = self.nil
        
    def search(self, x, key):
        '''
        Search for the node with the given key in the tree rooted at x.
        
        Parameters:
            - x: the root of the tree to search.
            - key: the key of the node to search.
            
        Returns:
            - The node with the given key if found, None otherwise.
        '''
        while x is not self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x
    
    def minrb(self, x):
        '''
        Find the minimum node in the tree rooted at x.
        
        Returns:
            - The minimum node if found, None otherwise.
        '''
        while x is not self.nil and x.left is not self.nil:
            x = x.left
        return x
    
    def maxrb(self, x):
        '''
        Find the maximum node in the tree rooted at x.
        
        Returns:
            - The maximum node if found, None otherwise.
        '''
        while x is not self.nil and x.right is not self.nil:
            x = x.right
        return x
    
    def successor(self, x):
        '''
        Find the successor of the node x.
        
        Returns:
            - The successor of the node x if found, None otherwise.
        '''
        if x.right is not self.nil:
            return self.bst_min(x.right)
        else:
            y = x.parent
            while y is not self.nil and x == y.right:
                x = y
                y = x.parent
            return y
    
    def predecessor(self, x):
        '''
        Find the predecessor of the node x.
        
        Returns:
            - The predecessor of the node x if found, None otherwise.
        '''
        if x.left is not self.nil:
            return self.bst_max(x.left)
        else:
            y = x.parent
            while y is not self.nil and x == y.left:
                x = y
                y = x.parent
            return y
    
    def _left_rotate(self, x):
        '''
        Left rotate the subtree rooted at x.
        
        Parameters:
            - x: the root of the subtree to be rotated.
        '''
        y = x.right
        if y is self.nil:
            return False
        x.right = y.left  # turn y's left subtree into x's right subtree
        if y.left is not self.nil:
            y.left.parent = x  # x becomes y's left subtree's parent
        y.parent = x.parent  # x's parent becomes y's parent
        if x.parent is self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        return True
    
    def _right_rotate(self, y):
        '''
        Right rotate the subtree rooted at y.

        
        Parameters:
            - y: the root of the subtree to be rotated.
        '''
        x = y.left
        if x is self.nil:
            return False
        y.left = x.right  # turn x's right subtree into y's left subtree
        if x.right is not self.nil:
            x.right.parent = y  # y becomes x's right subtree's parent
        x.parent = y.parent  # y's parent becomes x's parent
        if y.parent is self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insertrb(self, z):
        '''
        Insert node z into the tree.
        
        Returns:
            - True if insertion succeeds, False otherwise.
        '''
        y = self.nil  # y is the parent of z
        x = self.root  # x is the node being compared with z
        while x is not self.nil:
            y = x
            if z.key == x.key:
                return False
            elif z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y  # set y as z's parent
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil  # set z's children to nil
        z.right = self.nil
        z.set_red()  # set z's color to red
        self._insert_fixup(z)  # correct violation of red-black properties
        return True
    
    def _insert_fixup(self, z):
        '''
        Fix up the tree after insertion.
        
        Parameters:
            - z: the node inserted into the tree.
        '''
        while z.parent.is_red():  # z's parent is red
            if z.parent.parent is self.nil:  # z's parent is the root
                break
            if z.parent == z.parent.parent.left:  # z's parent is a left child
                y = z.parent.parent.right  # y is z's uncle
                if y.is_red():  # case 1: z's parent and uncle are both red
                    z.parent.set_black()
                    y.set_black()
                    z.parent.parent.set_red()
                    z = z.parent.parent
                else:
                    if z == z.parent.right:  # case 2: z's parent is red but uncle is black, left-right case
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.set_black()  # case 3: z's parent is red but uncle is black, left-left case
                    z.parent.parent.set_red()
                    self._right_rotate(z.parent.parent)
            else:  # same as above, but left and right are exchanged
                y = z.parent.parent.left
                if y.is_red():
                    z.parent.set_black()
                    y.set_black()
                    z.parent.parent.set_red()
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.set_black()
                    z.parent.parent.set_red()
                    self._left_rotate(z.parent.parent)
        self.root.set_black()

    def deleterb(self, z):
        '''
        Delete node z from the tree.
        
        Returns:
            - True if deletion succeeds, 
            - False if node z is not found in the tree.
        '''
        y = z
        y_original_color = y.color
        if z is self.nil:
            return False
        if z.left is self.nil:
            x = z.right
            self._transplant(z, z.right)  # replace z with its right child
        elif z.right is self.nil:
            x = z.left
            self._transplant(z, z.left)  # replace z with its left child
        else:
            y = self.minrb(z.right)  # y is z's successor
            y_original_color = y.color
            x = y.right
            if y != z.right:  # y is not z's right child
                self._transplant(y, y.right)  # replace y with its right child x
                y.right = z.right  # z's right child becomes y's right child
                y.right.parent = y
            else:
                x.parent = y  # in case x is nil
            self._transplant(z, y)  # replace z with y
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == RBNode.BLACK:
            self._delete_fixup(x)
        return True
    
    def _transplant(self, u, v):
        '''
        Replace subtree rooted at u with subtree rooted at v.
        
        Parameters:
            - u: the root of the subtree to be replaced.
            - v: the root of the replacing subtree.
        '''
        if u.parent is self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _delete_fixup(self, x):
        '''
        Fix up the tree after deletion.
        
        Parameters:
            - x: the node deleted from the tree.
        '''
        while x.parent is not self.nil and x.is_black():
            if x == x.parent.left:
                w = x.parent.right  # w is x's sibling
                if w.is_red():
                    w.set_black()  # case 1: x's sibling is red
                    x.parent.set_red()
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.is_black() and w.right.is_black():
                    w.set_red()  # case 2: x's sibling is black and both of w's children are black
                    x = x.parent
                else:
                    if w.right.is_black():  # case 3: x's sibling is black, w's left child is red and right child is black
                        w.left.set_black()
                        w.set_red()
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color  # case 4: x's sibling is black, w's right child is red
                    x.parent.set_black()
                    w.right.set_black()
                    self._left_rotate(x.parent)
                    x = self.root
            else:  # same as above, but left and right are exchanged
                w = x.parent.left
                if w.is_red():
                    w.set_black()
                    x.parent.set_red()
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.left.is_black() and w.right.is_black():
                    w.set_red()
                    x = x.parent
                else:
                    if w.left.is_black():
                        w.right.set_black()
                        w.set_red()
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.set_black()
                    w.left.set_black()
                    self._right_rotate(x.parent)
                    x = self.root
        x.set_black()
        
    def preorder_print(self, node=None, level=0, child=0, output_file=None, file=None):
        '''
        Preorder print the red-black tree to a file or the console.
        
        Parameters:
            - node: the current node to print, default is None, which means start from root.
            - level: the current level of the node, default is 0.
            - child: the left or right child of the parent, 0 for left, 1 for right, default is 0.
            - output_file: the file to write the output to, default is None, which means print to console.
        '''
        if node is None:
            node = self.root

        if output_file is not None and file is None:
            with open(output_file, 'w', encoding='utf-8') as f:
                self.preorder_print(node, level, child, output_file, f)
        elif file is not None:
            if node is not self.nil:
                color = "BLACK" if node.is_black() else "RED"
                file.write(f'level={level} child={child} {node.key}({color})\n')
                self.preorder_print(node.left, level + 1, 0, output_file, file)
                self.preorder_print(node.right, level + 1, 1, output_file, file)
            else:
                file.write(f'level={level} child={child} null\n')
        else:
            if node is not self.nil:
                color = "BLACK" if node.is_black() else "RED"
                print(f'level={level} child={child} {node.key}({color})')
                self.preorder_print(node.left, level + 1, 0)
                self.preorder_print(node.right, level + 1, 1)
            else:
                print(f'level={level} child={child} null')
    
    def initialize(self, filename):
        '''
        Initialize the red-black tree with the given file.
        
        Parameters:
            - filename: the file to initialize the red-black tree.
            
        Returns:
            - timerecord: a list of time records for every 100 insertions.
        '''
        timerecord = []
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return timerecord
            operation = lines[0].strip()
            if operation == 'INSERT':
                start = time.time()
                for index, line in enumerate(lines[1:], start=1):
                    word = line.strip().split(' ')
                    if len(word) == 2:
                        self.insertrb(RBNode(word[0], word[1]))
                    else:
                        return []
                    
                    if index % 100 == 0:  # record time for every 100 insertions
                        timerecord.append(time.time() - start)
                        start = time.time()
                
        self.preorder_print(output_file='rbt.txt')
        return timerecord
    
    def batch_op(self, filename):
        '''
        Perform batch insertion/deletion on the red-black tree with the given file.
        
        Parameters:
            - filename: the file to initialize the red-black tree.
            
        Returns:
            - timerecord: a list of time records for every 100 insertions.
        '''
        timerecord = []
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return timerecord
            operation = lines[0].strip()
            if operation == 'INSERT':
                start = time.time()
                for index, line in enumerate(lines[1:], start=1):
                    word = line.strip().split(' ')
                    if len(word) == 2:
                        self.insertrb(RBNode(word[0], word[1]))
                    else:
                        return []
                    
                    if index % 100 == 0:
                        timerecord.append(time.time() - start)
                        start = time.time()
            elif operation == 'DELETE':
                start = time.time()
                for index, line in enumerate(lines[1:], start=1):
                    word = line.strip().split(' ')
                    if len(word) == 1:
                        self.delete_word(word[0])
                    else:
                        return []
                    
                    if index % 100 == 0:
                        timerecord.append(time.time() - start)
                        start = time.time()
            else:
                return []
        
        self.preorder_print(output_file='rbt.txt')
        return timerecord
    
    def insert_word(self, en, cn):
        '''
        Insert a word into the red-black tree.
        '''
        if self.insertrb(RBNode(en, cn)):
            return "Insertion succeeded."
        else:
            return f"\"{en}\" already exists!"

    def delete_word(self, en):
        '''
        Delete a word from the red-black tree.
        '''
        z = self.search(self.root, en)
        if z is self.nil:
            return f"\"{en}\" not found!"
        else:
            self.deleterb(z)
            return "Deletion succeeded."
    
    def rangesearch(self, low, high, x=None, result=None):
        '''
        Search for words in the specified range [low, high].
        
        Parameters:
            - low: the lower bound of the range.
            - high: the upper bound of the range.
            - x: the current node in the traversal, default is the root.
            - result: list to store the result, default is an empty list.
        
        Returns:
            - A list of tuples, each tuple contains a word and its meaning.
        '''
        if x is None:
            x = self.root
        if result is None:
            result = []
        
        if x is not self.nil:
            self.rangesearch(low, high, x.left, result)
            if low <= x.key <= high:
                result.append((x.key, x.value))
            self.rangesearch(low, high, x.right, result)
        
            
        return result
    
    def singlesearch(self, word):
        '''
        Search for the given English word in the red-black tree.
        '''
        node = self.search(self.root, word)
        if node:
            return node.value
        else:
            return "Word not found!"


if __name__ == "__main__":

    # file operations
    rbt = RedBlackTree()
    time_init = rbt.initialize('./project1/1_initial.txt')
    # evaluate average initialization time
    # time_init = sum(time_init) / len(time_init)
    print(f'Initialization time: {time_init}')
    time_del = rbt.batch_op('./project1/2_delete.txt')
    print(f'Deletion time: {time_del}')
    time_insert = rbt.batch_op('./project1/3_insert.txt')
    print(f'Insertion time: {time_insert}')
    
    # # Single word query
    # meaning = rbt.singlesearch('cybernetic')
    # print(f'{meaning}')
    
    # # Range query
    # result = rbt.rangesearch('cuculliform', 'cumulocirrus')
    # for word, meaning in result:
    #     print(f'{word}: {meaning}')