class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
        
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left.values)
        if self.right != None:
            size += len(self.right.values)
        return size
    
    def lookup(self, target):
        if target == self.key:
            return self.values
        if target < self.key and self.left != None:
            return Node.lookup(self.left, target)
        if target > self.key and self.right != None:
            return Node.lookup(self.right, target)
        else:
            return []
               
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
        
    def __dump(self, node):
        if node == None:
            return
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)            # 1
        self.__dump(node.left)             # 3
        
    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, lookup):
        if self.root != None:
            return self.root.lookup(lookup)
            
    def height(self, node):
        if node is None:
            return 0
        left_height = self.height(node.left)
        right_height = self.height(node.right)        
        return 1 + max(left_height, right_height)
    
    def size(self, node):
        count = 0
        if node is None:
            return 0
        count += 1 + self.size(node.left) + self.size(node.right)
        return count

        