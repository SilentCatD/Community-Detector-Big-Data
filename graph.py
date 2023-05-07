class Graph:
    def __init__(self):
        self.nodes: dict[str, set[str]] = {}
        self.edges: set[tuple[str]] = set()

    @staticmethod
    def sorted_nodes(u: str, v: str):
        order = [u, v]
        order.sort()
        return tuple(order)

    def __create_node(self, u: str):
        if u not in self.nodes:
            self.nodes[u] = set()

    def __remove_node_relation(self, u: str, v: str):
        if u in self.nodes and v in self.nodes[u]:
            self.nodes[u].remove(v)

    def __add_node_relation(self, u: str, v: str):
        self.__create_node(u)
        self.nodes[u].add(v)

    def add_edge(self, u: str, v: str):
        sorted_order = Graph.sorted_nodes(u, v)
        if u == v or sorted_order in self.edges:
            return
        self.__add_node_relation(u, v)
        self.__add_node_relation(v, u)
        self.edges.add(sorted_order)

    def remove_edge(self, u: str, v: str):
        sorted_order = Graph.sorted_nodes(u, v)
        if u == v or sorted_order not in self.edges:
            return
        self.edges.remove(sorted_order)
        self.__remove_node_relation(u, v)
        self.__remove_node_relation(v, u)

    def get_communities(self) -> list[tuple[str]]:
        visited = set()
        communities: list[tuple[str]] = []
        for node in self.nodes.keys():
            if node in visited:
                continue
            community: list[str] = [node]
            queue: list[str] = [node]
            visited.add(node)
            while queue:
                current_node = queue.pop(0)
                for adjacent_node in self.nodes[current_node]:
                    if adjacent_node not in visited:
                        queue.append(adjacent_node)
                        visited.add(adjacent_node)
                        community.append(adjacent_node)
            community = sorted(community)
            communities.append(tuple(community))
        communities = sorted(communities, key=lambda x: (len(x), x[0]))
        return communities

    def copy(self):
        new_graph = Graph()
        new_graph.edges = set(edge for edge in self.edges)
        new_nodes: dict[str, set[str]] = {}
        for node in self.nodes.keys():
            new_nodes[node] = set(adjacent for adjacent in self.nodes[node])
        new_graph.nodes = new_nodes
        return new_graph

    def count_nodes(self) -> int:
        return len(self.nodes)

    def count_edges(self) -> int:
        return len(self.edges)

    def connected(self, node_u, node_v) -> bool:
        sorted_order = Graph.sorted_nodes(node_u, node_v)
        return sorted_order in self.edges


if __name__ == '__main__':
    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('D', 'G')
    graph.add_edge('D', 'E')
    graph.add_edge('D', 'F')
    graph.add_edge('G', 'F')
    graph.add_edge('E', 'F')
    graph.remove_edge('B', 'D')

    print(graph.nodes)
    print(graph.edges)
    print(graph.get_communities())

    copied = graph.copy()
    copied.remove_edge('A', 'C')
    print(graph.edges)
    print(copied.edges)
