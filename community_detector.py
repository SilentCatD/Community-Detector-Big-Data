from abc import abstractmethod
import networkx as nx
from graph import Graph
from networkx.algorithms.community import girvan_newman
from networkx.algorithms.community import modularity
from betweenness_calculator import SelfImplementedBetweennessCalculator


class CommunityDetector:
    def detect(self, file_name: str = None) -> list[tuple[str]]:
        result = self._detect()
        result = sorted(result, key=lambda x: (len(x), x[0]))
        if file_name:
            CommunityDetector.__out_put_to_file(result, file_name)
        return result

    @abstractmethod
    def _detect(self) -> list[tuple[str]]:
        raise NotImplementedError()

    @staticmethod
    def __out_put_to_file(communities: list[tuple[str]], file_name: str):
        with open(file_name, 'w') as f:
            for community in communities:
                community_repr = ', '.join(f"'{reformatted}'" for reformatted in community) + '\n'
                f.write(community_repr)

    @staticmethod
    def benchmark_communities(community_a_file: str, community_b_file: str):
        with open(community_a_file, 'r') as f:
            community_a = f.read()
        with open(community_b_file, 'r') as f:
            community_b = f.read()

        assert community_a == community_b
        print('============================================')
        print('detected communities identical')
        print('============================================')


class SelfImplementedCommunityDetector(CommunityDetector):
    def __init__(self, graph: Graph):
        self.graph = graph

    def _detect(self) -> list[tuple[str]]:
        graph_clone = self.graph.copy()
        max_modularity = -1
        max_modularity_communities = None
        print('============================================')
        print('detecting communities...')
        while True:
            if graph_clone.count_edges() == 0:
                break
            SelfImplementedCommunityDetector.__girvan_newman(graph_clone)
            communities_modularity = self.__modularity(graph_clone.get_communities())
            if communities_modularity > max_modularity:
                max_modularity = communities_modularity
                max_modularity_communities = graph_clone.get_communities()
        print('============================================')

        if max_modularity_communities is None:
            return []
        return max_modularity_communities

    @staticmethod
    def __girvan_newman(graph: Graph):
        community_count = len(graph.get_communities())
        while True:
            if graph.count_edges() == 0 or len(graph.get_communities()) > community_count:
                break
            edge_betweenness_calculator = SelfImplementedBetweennessCalculator(graph)
            edge_betweenness = edge_betweenness_calculator.calculate_betweenness()
            highest_betweenness_edge = edge_betweenness[0][0]
            graph.remove_edge(highest_betweenness_edge[0], highest_betweenness_edge[1])

    def __modularity(self, communities: list[tuple[str]]):
        accumulate = 0
        m = len(self.graph.edges)
        for community in communities:
            for i in community:
                for j in community:
                    a_ij = 1 if self.graph.connected(i, j) else 0
                    k_i = len(self.graph.nodes[i])
                    k_j = len(self.graph.nodes[j])
                    accumulate += (a_ij - (k_i * k_j) / (2 * m))
        accumulate *= (1 / (2 * m))
        return accumulate


class NetworkxCommunityDetector(CommunityDetector):
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def _detect(self) -> list[tuple[str]]:
        graph_clone = self.graph.copy()
        comp = girvan_newman(graph_clone)
        max_modularity = - 1
        max_modularity_communities = None

        print('============================================')
        print('detecting communities...')
        while True:
            try:
                communities = next(comp)
            except StopIteration:
                break
            communities_modularity = modularity(graph_clone, communities)
            if communities_modularity > max_modularity:
                max_modularity = communities_modularity
                max_modularity_communities = communities
        print('============================================')
        if max_modularity_communities is None:
            return []
        result = list(tuple(sorted(str(node) for node in c)) for c in
                      max_modularity_communities)
        return result
