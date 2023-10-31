class BSTNode:
    def __init__(self, key, value, left=None, right=None, parent=None):
        '''
        Initialize a binary search tree node.
        
        Parameters:
            - key: the key of the node, English word (string) in this case.
            - value: the value of the node, Chinese translation (string) of the English word.
            - left: the left child of the node, default is None.
            - right: the right child of the node, default is None.
            - parent: the parent of the node, default is None.
        '''
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        
        
    def __str__(self):
        '''
        Return string representation of the node.
        '''
        return str(self.key) + ':' + str(self.value)


class BSTree:
    '''
    A binary search tree class.
    '''
    def __init__(self):
        self.root = None
        
    def bst_search(self, x, key):
        '''
        Search for the node with the given key in the tree rooted at x.
        
        Parameters:
            - self: the binary search tree to search.
            - x: the root of the tree to search.
            - key: the key of the node to search.
            
        Returns:
            - The node with the given key if found, None otherwise.
        '''
        while x != None and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def bst_min(self, x):
        '''
        Find the minimum node in the tree rooted at x.
        
        Returns:
            - The minimum node if found, None otherwise.
        '''
        while x and x.left:
            x = x.left
        return x

    def bst_max(self):
        '''
        Find the maximum node in the tree rooted at x.
        
        Returns:
            - The maximum node if found, None otherwise.
        '''
        while x and x.right:
            x = x.right
        return x

    def bst_successor(self, x):
        '''
        Find the successor of the node x.
        
        Returns:
            - The successor of the node x if found, None otherwise.
        '''
        if x.right:
            return self.bst_min(x.right)
        else:
            y = x.parent
            while y and x == y.right:
                x = y
                y = x.parent
            return y

    def bst_insert(self, z):
        '''
        Insert node z into the tree.
        
        Returns:
            - True if insertion succeeds, False otherwise.
        '''
        y = None
        x = self.root
        while x != None:
            y = x
            if z.key == x.key:
                return False
            elif z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        return True
        
    def bst_delete(self, z):
        '''
        Delete node z from the tree.
        
        Returns:
            - True if deletion succeeds, False if node z is not found in the tree.
        '''
        if z is None:
            return False
        if z.left == None:
            self.bst_transplant(z, z.right)
        elif z.right == None:
            self.bst_transplant(z, z.left)
        else:
            y = self.bst_min(z.right)
            if y != z.right:
                self.bst_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.bst_transplant(z, y)
            y.left = z.left
            y.left.parent = y
        return True
    
    def bst_transplant(self, u, v):
        '''
        Replace subtree rooted at u with subtree rooted at v.
        
        Parameters:
            - u: the root of the subtree to be replaced.
            - v: the root of the replacing subtree.
        '''
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v != None:
            v.parent = u.parent
    
    def preorder_print(self, x):
        '''
        Print the node in preorder.
    
        Parameters:
            - x: the node to be printed.
        '''
        if x is not None:
            print(x.key, x.value)
            self.preorder_print(x.left)
            self.preorder_print(x.right)