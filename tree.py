from graph import Graph


class TreeNode:
    def __init__(self, name: str):
        self.incoming_nodes: set[TreeNode] = set()
        self.outgoing_nodes: set[TreeNode] = set()
        self.name = name
        self.shortest_path_count = 0

    def add_incoming_node(self, node):
        self.incoming_nodes.add(node)
        parent_shortest_path = node.shortest_path_count
        if parent_shortest_path == 0:
            parent_shortest_path = 1
        self.shortest_path_count += parent_shortest_path

    def add_outgoing_node(self, node):
        self.outgoing_nodes.add(node)

    def is_root(self) -> bool:
        return len(self.incoming_nodes) == 0

    def is_leaf(self) -> bool:
        return len(self.outgoing_nodes) == 0

    def is_isolated(self) -> bool:
        return self.is_leaf() and self.is_root()


class Tree:
    def __init__(self, root: TreeNode = None):
        self.root = root
        self.name_to_node: dict[str, TreeNode] = {root.name: root}
        self.edge_betweenness: dict[tuple[str], float] = {}

    @staticmethod
    def from_graph(graph: Graph, source: str):
        # prevent going up
        traveled_graph_nodes: set[str] = set()

        # prevent going same level
        next_lvl_graph_nodes: set[str] = set()

        next_lvl_graph_nodes.add(source)
        tree_root = TreeNode(source)
        result_tree = Tree(tree_root)

        while next_lvl_graph_nodes:
            next_level_graph_nodes = set()

            for graph_node in next_lvl_graph_nodes:
                tree_node = result_tree.name_to_node[graph_node]
                for adjacent_graph_node in graph.nodes[graph_node]:
                    if adjacent_graph_node not in traveled_graph_nodes and adjacent_graph_node not in \
                            next_lvl_graph_nodes:
                        adjacent_tree_node = result_tree.get_or_create_node(adjacent_graph_node)
                        adjacent_tree_node.add_incoming_node(tree_node)
                        tree_node.add_outgoing_node(adjacent_tree_node)
                        next_level_graph_nodes.add(adjacent_graph_node)

            for graph_node in next_lvl_graph_nodes:
                traveled_graph_nodes.add(graph_node)

            next_lvl_graph_nodes = next_level_graph_nodes

        result_tree.calculate_edge_betweenness()
        return result_tree

    def calculate_edge_betweenness(self):
        for node in self.root.outgoing_nodes:
            self.__calculate_edge_betweenness(self.root, node)

    def __calculate_edge_betweenness(self, node_u: TreeNode, node_v: TreeNode) -> float:
        ordered_name = Graph.sorted_nodes(node_u.name, node_v.name)
        if node_u.is_root():
            scale = 1
        else:
            scale = node_u.shortest_path_count / node_v.shortest_path_count

        if node_v.is_leaf():
            self.edge_betweenness[ordered_name] = scale
            return scale

        accumulate = 1
        for node in node_v.outgoing_nodes:
            accumulate += self.__calculate_edge_betweenness(node_v, node)
        accumulate *= scale
        self.edge_betweenness[ordered_name] = accumulate
        return accumulate

    def __update_node_map(self, name: str, tree_node: TreeNode):
        assert name not in self.name_to_node
        self.name_to_node[name] = tree_node

    def get_or_create_node(self, name: str) -> TreeNode:
        node = self.name_to_node.get(name)
        if node is None:
            node = TreeNode(name)
            self.__update_node_map(name, node)
        return node

    def display(self):
        if self.edge_betweenness:
            print(f'edge betweenness: {self.edge_betweenness}')
        for node_name, node in self.name_to_node.items():
            node_type = ''
            if node.is_isolated():
                node_type += '- isolated'
            elif node.is_root():
                node_type += '- root'
            elif node.is_leaf():
                node_type += '- leaf'
            print(f'node {node_name} {node_type} - shortest_path: {node.shortest_path_count}')
            print('\tincoming: ', end='')
            for incoming in node.incoming_nodes:
                print(incoming.name, end=', ')
            print()
            print('\toutgoing: ', end='')
            for outgoing in node.outgoing_nodes:
                print(outgoing.name, end=', ')
            print()


if __name__ == '__main__':
    # simple graph
    simple_graph = Graph()
    simple_graph.add_edge('A', 'B')
    simple_graph.add_edge('A', 'D')
    simple_graph.add_edge('B', 'E')
    simple_graph.add_edge('D', 'E')
    simple_graph.add_edge('B', 'C')
    simple_graph.add_edge('C', 'F')
    simple_graph.add_edge('E', 'F')

    tree = Tree.from_graph(simple_graph, source='E')
    tree.display()
