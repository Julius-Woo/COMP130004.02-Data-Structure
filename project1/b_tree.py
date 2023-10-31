import os
import time

class BTNode:
    '''
    Initialize a B-tree node.
    
    Parametters:
        - n: number of keys stored in the tree.
        - keys: list of keys (English word) stored in the x, stored in ascending order.
        - values: list of values (Chinese translation) stored in the x, corresponding to the keys.
        - leaf: a boolean value indicating whether the x is a leaf, default is True.
        - c: list of points to child nodes.
    '''
    def __init__(self, n=0, keys=None, values=None, isleaf=True, c=None):
        self.n = n
        self.keys = keys if keys is not None else []
        self.values = values if values is not None else []
        self.isleaf = isleaf
        self.c = c if c is not None else []
    
    def is_full(self, t):
        '''
        Check whether the x is full. Return True if the x is full, False otherwise.
        '''
        return self.n == 2*t - 1

class BTree:
    def __init__(self, t):
        '''
        Initialize a B-tree.
        
        Parameters:
            - t: order of the B-tree, i.e., each x (except the root) has at least t-1 keys and at most 2t-1 keys.
        '''
        self.root = BTNode(isleaf=True)
        self.t = t
        
    def search(self, key, x=None):
        '''
        Search for the x with the given key in the tree rooted at x.
        
        Parameters:
            - x: the root of the tree to search, default is None, which means start from root.
            - key: the key of the x to search.
            
        Returns:
            - (y,i): a tuple of the node y and the index i such that y.keys[i] is the given key.
            - None: if the given key is not in the tree.
        '''
        if x is None:
            x = self.root
        i = 0
        while i < x.n and key > x.keys[i]:  # find the smallest i such that key <= x.keys[i]
            i += 1
        if i < x.n and key == x.keys[i]:  # the key is in x
            return x, i
        elif x.isleaf:
            return None  # the key is not in the tree
        else:
            return self.search(key, x.c[i])  # the key may be in the subtree rooted at x.c[i]

    def insertb(self, key, value):
        '''
        Insert the given key and its value into the B-tree.
        
        Parameters:
            - key: the key of the x to insert.
            - value: the value of the x to insert.
        '''
        r = self.root
        if not self.search(key, r):  # if the key is not in the tree
            if r.is_full(self.t):
                s = self._split_root()
                self._insert_nonfull(s, key, value)
            else:
                self._insert_nonfull(r, key, value)
            return True
        return False  # the key is already in the tree

    def _insert_nonfull(self, x, key, value):
        '''
        Insert the given key and its value into the non-full x.
        
        Parameters:
            - x: the non-full x to insert.
            - key: the key of the x to insert.
            - value: the value of the x to insert.
            
        Returns:
            - True: if the key is successfully inserted.
            - False: if the key is already in the tree.
        '''
        i = x.n - 1
        if x.isleaf:
            while i >= 0 and key < x.keys[i]:  # find the position to insert
                i -= 1
            if i >= 0 and key == x.keys[i]:
                return False  # the key is already in the tree
            x.keys.insert(i+1, key)  # insert key into x
            x.values.insert(i+1, value)
            x.n += 1
            return True
        else:
            while i >= 0 and key < x.keys[i]:  # find the child to insert
                i -= 1
            if i >= 0 and key == x.keys[i]:
                return False  # the key is already in the tree
            i += 1  # i is the index of the child to insert
            if x.c[i].is_full(self.t):
                self._split_child(x, i)
                if key > x.keys[i]:  # insert into the new child
                    i += 1
            return self._insert_nonfull(x.c[i], key, value)

    def _split_child(self, x, i):
        '''
        Split the i-th child (full) of x.

        Parameters:
            - x: the parent of the child to split.
            - i: the index of the child to split.
        '''
        t = self.t
        y = x.c[i]  # the full child to split
        z = BTNode(n=t-1, isleaf=y.isleaf, keys=y.keys[t:], values=y.values[t:])   # z takes right half of y's keys (greatest t-1 keys)
        if not y.isleaf:  # if y is not a leaf, z also takes half of y's children
            z.c = y.c[t:]
            y.c = y.c[:t]
        y.n = t - 1
        
        # Insert z into x at index i+1
        x.c.insert(i+1, z)
        # Insert y's median key and value into x at index i
        x.keys.insert(i, y.keys[t-1])
        x.values.insert(i, y.values[t-1])
        x.n += 1
        
        y.keys = y.keys[:t-1]  # y's first half of keys (smallest t-1 keys)
        y.values = y.values[:t-1]

    def _split_root(self):
        '''
        Split the root of the tree.
        '''
        s = BTNode(isleaf=False)  # create a new root s
        s.c.append(self.root)  # set the old root as s's first child
        self.root = s  # set s as the new root
        self._split_child(s, 0)  # split the old root (now s's first child)
        return s

    def deleteb(self, key, x=None):
        '''
        Delete the given key from the tree rooted at x.
        
        Parameters:
            - x: the root of the subtree, default is None, which means start from root.
            - key: the key to be deleted.
            
        Returns:
            - True if deletion succeeds, 
            - False if node z is not found in the tree.
        '''
        if x is None:
            x = self.root
            if self.search(key, x) is None:
                return False
        t = self.t
        i = 0
        while i < x.n and key > x.keys[i]:
            i += 1
        
        # Case 1: x is a leaf, delete directly
        if x.isleaf:
            if i < x.n and x.keys[i] == key:
                x.keys.pop(i)
                x.values.pop(i)
                x.n -= 1
                return True
            return False  # the key is not in the tree at all
        
        # Case 2: x is an internal node and the key is in x
        if i < x.n and x.keys[i] == key:
            return self._delete_internal_node(x, key, i)
        # Recursively calling delete on x.c[i]
        elif x.c[i].n >= t:
            return self.deleteb(key, x.c[i])
        # Case 3: x is an internal node and the key is not in x, its child x.c[i] has less than t keys
        else:
            if i != 0 and x.c[i - 1].n >= t:   # Case 3a: x.c[i-1] has at least t keys
                self._delete_sibling(x, i, -1)
            elif i + 1 < len(x.c) and x.c[i + 1].n >= t:   # Case 3a: or x.c[i+1] has at least t keys
                self._delete_sibling(x, i)
            else:  # Case 3b: x.c[i] and each of x.c[i]’s immediate siblings have t − 1 keys
                if i != x.n:  # if x.c[i] is not the last child of x
                    self._delete_merge(x, i)
                    if x.n == 0:   # After merge, check if x is still the root
                        return self.deleteb(key, self.root)
                else:
                    self._delete_merge(x, i, -1)
                    if x.n == 0:
                        return self.deleteb(key, self.root)
                    return self.deleteb(key, x.c[i-1])
            return self.deleteb(key, x.c[i])

    def _delete_internal_node(self, x, key, i):
        '''
        Delete the given key from the internal node x.
        
        Parameters:
            - x: the internal node to delete.
            - key: the key to be deleted.
            - i: the index of the key to be deleted in x.keys.
        '''
        t = self.t
        if x.c[i].n >= t:  # Case 2a: x.c[i] has at least t keys
            result = self._delete_predecessor(x.c[i])
            if result is not None:
                x.keys[i], x.values[i] = result
                return True
            return False
        elif x.c[i + 1].n >= t:  # Case 2b: x.c[i+1] has at least t keys
            result = self._delete_successor(x.c[i + 1])
            if result is not None:
                x.keys[i], x.values[i] = result
                return True
            return False
        else:
            self._delete_merge(x, i)  # Case 2c: both x.c[i] and x.c[i+1] have only t-1 keys
            # After merge, check if x is still the root
            if x.n == 0:
                return self.deleteb(key, self.root)
            return self.deleteb(key, x.c[i])

    def _delete_predecessor(self, x):
        '''
        Delete the greatest key the given node x.
        '''
        if x.isleaf:
            x.n -= 1
            return x.keys.pop(), x.values.pop()
        
        l = x.n  # the index of the last child of x
        # if x is not a leaf, continue to find the real predecessor in x.c[l]
        if x.c[l].n < self.t:  # if x.c[l] has only t-1 keys
            if x.c[l-1].n >= self.t:  # if x.c[l-1] has at least t keys
                self._delete_sibling(x, l, -1)  # borrow a key from x.c[l-1]
                return self._delete_predecessor(x.c[l])
            else:
                self._delete_merge(x, l, -1)  # merge x.c[l] and x.c[l-1] into x.c[l]
                return self._delete_predecessor(x.c[l-1])
        else:
            return self._delete_predecessor(x.c[l])

    def _delete_successor(self, x):
        '''
        Delete the smallest key the given node x.
        '''
        if x.isleaf:
            x.n -= 1
            return x.keys.pop(0), x.values.pop(0)
        
        # if x is not a leaf, continue to find the real successor in x.c[0]
        if x.c[0].n < self.t:  # if x.c[0] has only t-1 keys
            if x.c[1].n >= self.t:  # if x.c[1] has at least t keys
                self._delete_sibling(x, 0)  # borrow a key from x.c[1]
            else:
                self._delete_merge(x, 0)  # merge x.c[0] and x.c[1] into x.c[0]
        return self._delete_successor(x.c[0])

    def _delete_merge(self, x, i, j = 1):
        '''
        Merge the key at index i and child i+j of x with child i.
        
        Parameters:
            - x: the parent of the children to merge.
            - i: the index of the children to merge.
            - j: indicate the left or right sibling of the child to merge, i.e., x.c[i] and x.c[i+j]. default to 1.
        '''
        if j == 1:
            y = x.c[i]  # x.c[i] is the child to merge
            z = x.c[i + 1]  # x.c[i+1] is the sibling of the child to merge
            y.keys.append(x.keys.pop(i))  # y gets key[i] from x
            y.values.append(x.values.pop(i))
            y.keys.extend(z.keys)  # y gets all keys and values from z
            y.values.extend(z.values)
            if not y.isleaf:  # if y is not a leaf, y gets all children from z
                y.c.extend(z.c)
            y.n = len(y.keys)
            x.c.pop(i + 1)  # delete z from x
            x.n -= 1
            if x == self.root and x.n == 0: # if x is the root and x is empty, set y as the new root
                self.root = y
        else:
            y = x.c[i]  # x.c[i] is the child to merge
            z = x.c[i - 1]  # x.c[i-1] is the sibling of the child to merge
            y.keys.insert(0, x.keys.pop(i - 1))  
            y.values.insert(0, x.values.pop(i - 1))
            y.keys[:0] = z.keys # y gets all keys and values from z
            y.values[:0] = z.values
            if not y.isleaf:  # if y is not a leaf, y gets all children from z
                y.c[:0] = z.c
            y.n = len(y.keys)
            x.c.pop(i - 1)  # delete z from x
            x.n -= 1
            if x == self.root and x.n == 0:  # if x is the root and x is empty, set y as the new root
                self.root = y

    def _delete_sibling(self, x, i, j=1):
        '''
        Borrow a key from the i+j-th child of x and append it to the i-th child of x.
        
        Parameters:
            - x: the parent node.
            - i: the index of the child to lend a key.
            - j: indicate the left or right sibling of the child to borrow a key, i.e., x.c[i] and x.c[i+j]. default to 1.
        '''
        if j==1:  # borrow a key from the right sibling
            j = i + 1
            y = x.c[i]
            z = x.c[j]
            y.keys.append(x.keys[i])  # y gets key[i] from x
            y.values.append(x.values[i])  # y gets value[i] from x
            if not y.isleaf:  # if y is not a leaf, y gets the first child from z
                y.c.append(z.c.pop(0))
            x.keys[i] = z.keys.pop(0)  # x gets the first key from z
            x.values[i] = z.values.pop(0)  # x gets the first value from z
        else:  # borrow a key from the left sibling
            j = i - 1
            y = x.c[i]
            z = x.c[j]
            y.keys.insert(0, x.keys[i - 1])  # y gets key[i-1] from x
            y.values.insert(0, x.values[i - 1])  # y gets value[i-1] from x
            if not y.isleaf:  # if y is not a leaf, y gets the last child from z
                y.c.insert(0, z.c.pop())
            x.keys[i - 1] = z.keys.pop()  # x gets the last key from z
            x.values[i - 1] = z.values.pop()  # x gets the last value from z
        y.n += 1
        z.n -= 1
    
    def preorder_print(self, node=None, level=0, child=0, output_file=None, file=None):
        '''
        Preorder print the B-tree to a file.
        
        Parameters:
            - node: the current node to print, default is None, which means start from root.
            - level: the current level of the node, default is 0.
            - child: the child's index, default is 0.
            - output_file: the file to write the output to, default is None, which means write to console.
        '''
        if node is None:
            node = self.root
        
        if output_file is not None and file is None:
            with open(output_file, 'w', encoding='utf-8') as f:
                self.preorder_print(node, level, child, output_file, f)
        elif file is not None:
            keys_str = '/'.join(map(str, node.keys))
            file.write(f"level={level} child={child} /{keys_str}/\n")
            if not node.isleaf:
                for i, child_node in enumerate(node.c):
                    self.preorder_print(child_node, level+1, i, output_file, file)
        else:
            keys_str = '/'.join(map(str, node.keys))
            print(f"level={level} child={child} /{keys_str}/")
            if not node.isleaf:
                for i, child_node in enumerate(node.c):
                    self.preorder_print(child_node, level+1, i, output_file)

    
    def initialize(self, filename):
        '''
        Initialize the B-tree with the given file.
        
        Parameters:
            - filename: the file to initialize the B-tree.
            
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
                        self.insertb(word[0], word[1])
                    else:
                        return []
                    
                    if index % 100 == 0:  # record time for every 100 insertions
                        timerecord.append(time.time() - start)
                        start = time.time()
                
        self.preorder_print(output_file='bt.txt')
        return timerecord
    
    def batch_op(self, filename):
        '''
        Perform batch operations with the given file.
        
        Parameters:
            - filename: the file to perform batch operations.
            
        Returns:
            - timerecord: a list of time records for every 100 operations.
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
                        self.insertb(word[0], word[1])
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
                        self.deleteb(word[0])
                    else:
                        return []
                    
                    if index % 100 == 0:
                        timerecord.append(time.time() - start)
                        start = time.time()
            else:
                return []
        
        self.preorder_print(output_file='bt.txt')
        return timerecord
        
    def insert_word(self, en, cn):
        '''
        Insert the given English word and its Chinese translation into the B-tree.
        '''
        if self.insertb(en, cn):
            return "Insertion succeeded."
        else:
            return f"\"{en}\" already exists!"
        
    def delete_word(self, en):
        '''
        Delete the given English word from the B-tree.
        '''
        if self.deleteb(en):
            return "Deletion succeeded."
        else:
            return f"\"{en}\" not found!"
        
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
        
        i = 0
        while i < x.n and low > x.keys[i]:
            i += 1

        if x.isleaf:
            while i < x.n and x.keys[i] <= high:
                result.append((x.keys[i], x.values[i]))
                i += 1
        else:
            if i >= x.n or x.keys[i] > high:
                self.rangesearch(low, high, x.c[i], result)
            else:
                while i < x.n and x.keys[i] <= high:
                    self.rangesearch(low, high, x.c[i], result)
                    result.append((x.keys[i], x.values[i]))
                    i += 1
                if x.keys[i-1] < high:
                    self.rangesearch(low, high, x.c[i], result)

        return result
        
    def singlesearch(self, word):
        '''
        Search for the given English word in the B-tree. Return the Chinese translation if found, otherwise return "Word not found!".
        '''
        result = self.search(word)
        if result:
            return result[0].values[result[1]]
        else:
            return "Word not found!"


if __name__ == "__main__":

    # file operations
    bt = BTree(t=10)
    time_init = bt.initialize('./project1/1_initial.txt')
    print(f'Initialization time: {time_init}')
    time_del = bt.batch_op('./project1/2_delete.txt')
    print(f'Deletion time: {time_del}')
    time_insert = bt.batch_op('./project1/3_insert.txt')
    print(f'Insertion time: {time_insert}')
    
    # Single word query
    meaning = bt.singlesearch('cybernetic')
    print(f'{meaning}')
    
    # Range query
    result = bt.rangesearch('cuculliform', 'culmination')
    for word, meaning in result:
        print(f'{word}: {meaning}')