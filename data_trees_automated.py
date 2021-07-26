from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import random


def randrange_list(limit):
    if limit <= 1:
        return [0]
    else:
        # random.randint() instead of random.randrange() because
        # range() prevents the limit from being used anyway (which
        # would cause an IndexError in tree.create_nodes())
        n1 = random.randint(0, limit)
        n2 = random.randint(0, limit)

        # Don't let the two numbers be the same
        while n1 == n2:
            n2 = random.randint(0, limit)

        if n1 < n2:
            return [i for i in range(n1, n2)]
        elif n1 > n2:
            return [i for i in range(n2, n1)]


class Tree:
    def __init__(self):
        # for self.count_nodes()
        self.node_count = 0
        # The maximum amount of nodes in a tree is 15 (14 here because
        # we're counting the root node)
        self.nodes = random.randint(0, 14)

    def tree_sum(self, root):
        '''
        Given that the last character of the node name contains the
        data (a single integer, 0 or 1 in this case), return the sum
        of the data of all the nodes.
        '''
        root_data = int(root.name[-1])
        return root_data + (sum([self.tree_sum(root.children[i])
                            for i in range(len(root.children))]))

    def create_nodes(self, root):
        '''
        Automatically creates the nodes of the tree according to
        self.nodes, which specifies how many nodes should be created.
        '''
        # If there are no nodes left to assign, pass
        if self.nodes <= 0:
            pass
        else:
            # if-statement prevents the two for-loops here from
            # generating an IndexError.
            if self.nodes >= 5:
                child_num = random.randint(1, 5)
            else:
                child_num = random.randint(1, self.nodes)

            list = []
            for i in range(child_num):
                # data is either 0 or 1
                data = round(random.random())
                list.append(Node(f'n{str(i)} {data}'))
                self.nodes -= 1
            root.children = list

            for i in randrange_list(child_num):
                self.create_nodes(root.children[i])

    def count_nodes(self, root):
        '''Returns how many nodes there are in the tree.'''
        # Has to be recursive to count the nodes outside of the root
        # node's children.
        for i in range(len(root.children)):
            self.count_nodes(root.children[i])

        self.node_count += 1
        return self.node_count

    def count_uni_trees(self, root):
        '''
        Returns the number of universal trees found in the tree formed
        by the root node.
        '''
        x = True

        # For-loop compares the children's data to the parent's.
        # If the data of any of the children is different, x gets
        # assigned to False.
        for i in range(len(root.children)):
            if (root.children[i] != None and
                root.children[i].name[-1] != root.name[-1]):
                x = False
                break

        # Builds up the answer for how many universal trees there are
        # through recursion with the "return 1 + s"/"return 0 + s"
        # statements.
        s = sum([self.count_uni_trees(root.children[i])
                 for i in range(len(root.children))])

        if x is True:
            '''
            DEPENDENCY WARNING: self.node_count is only valid when
            count_nodes() has been run before this method.
            '''
            if self.node_count - 1 == s:
                s += 1
            return 1 + s
        else:
            return 0 + s


# Initialize the root as 'r' with either a 0 or 1 as its data (ex: 'r 1')
root = Node(f'r {round(random.random())}')
tree = Tree()
tree.create_nodes(root)

print(RenderTree(root))
print(f'DATA SUM: {tree.tree_sum(root)}')
print(f'NODE COUNT: {tree.count_nodes(root)}')
print(f'UNI. TREES: {tree.count_uni_trees(root)}')
