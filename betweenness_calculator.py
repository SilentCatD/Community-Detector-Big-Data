from abc import abstractmethod
from graph import Graph
from tree import Tree
from networkx.algorithms.centrality import edge_betweenness_centrality
import networkx as nx


class BetweennessCalculator:
    def calculate_betweenness(self, file_name: str = None) -> list[tuple[tuple[str], float]]:
        sorted_results = self._calculate_betweenness()
        sorted_results = sorted(sorted_results, key=lambda x: (-x[1], x[0][0], x[0][1]))
        if file_name:
            BetweennessCalculator.__output_to_file(sorted_results, file_name)
        return sorted_results

    @abstractmethod
    def _calculate_betweenness(self) -> list[tuple[tuple[str], float]]:
        raise NotImplementedError()

    @staticmethod
    def __output_to_file(sorted_results: list[tuple[tuple[str], float]], file_name: str):
        with open(file_name, 'w') as f:
            for result in sorted_results:
                f.write(f"('{result[0][0]}', '{result[0][1]}'), {result[1]}\n")

    @staticmethod
    def mse_benchmark_betweenness(betweenness_file_a: str, betweenness_file_b: str) -> float:
        with open(betweenness_file_a, 'r') as file:
            betweenness_a = file.readlines()
        with open(betweenness_file_b, 'r') as file:
            betweenness_b = file.readlines()
        assert len(betweenness_a) == len(betweenness_b)
        if len(betweenness_a) == 0:
            print('no edge betweenness')
            return 0.0
        accumulate = 0
        for index, entries in enumerate(betweenness_a):
            split_a = betweenness_a[index].split(',')
            split_b = betweenness_b[index].split(',')
            value_a = float(split_a[-1].strip())
            value_b = float(split_b[-1].strip())
            accumulate += pow(value_a - value_b, 2)
        accumulate /= len(betweenness_a)
        print('============================================')
        print(f'betweenness mse: {accumulate}')
        print('============================================')
        return accumulate


class SelfImplementedBetweennessCalculator(BetweennessCalculator):
    def __init__(self, graph: Graph):
        self.graph = graph

    def _calculate_betweenness(self) -> list[tuple[tuple[str], float]]:
        edges_betweenness_dict: dict[tuple[str], float] = {}
        for root_node in self.graph.nodes.keys():
            root_based_tree = Tree.from_graph(self.graph, source=root_node)
            edge_betweenness = root_based_tree.edge_betweenness
            for calculated_edge in edge_betweenness.keys():
                if calculated_edge in edges_betweenness_dict:
                    edges_betweenness_dict[calculated_edge] += edge_betweenness[calculated_edge] / 2
                else:
                    edges_betweenness_dict[calculated_edge] = edge_betweenness[calculated_edge] / 2
        results = list(edges_betweenness_dict.items())
        return results


class NetworkXBetweennessCalculator(BetweennessCalculator):
    def __init__(self, networkx_graph: nx.Graph):
        self.networkx_graph = networkx_graph

    def _calculate_betweenness(self) -> list[tuple[tuple[str], float]]:
        edges_betweenness_dict = edge_betweenness_centrality(self.networkx_graph, normalized=False)
        edges_betweenness_lib = list(edges_betweenness_dict.items())
        converted_betweenness: list[tuple[tuple[str], float]] = []
        for edge_betweenness in edges_betweenness_lib:
            node_u = edge_betweenness[0][0]
            node_v = edge_betweenness[0][1]
            betweenness_value = float(edge_betweenness[1])
            sorted_edge = Graph.sorted_nodes(node_u, node_v)
            entries: tuple[tuple[str], float] = (sorted_edge, betweenness_value)
            converted_betweenness.append(entries)
        return converted_betweenness
