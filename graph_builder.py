from graph import Graph
import networkx as nx
from abc import abstractmethod
import pandas as pd
from tqdm import tqdm


class GraphBuilder:
    @abstractmethod
    def add_edge(self, node_u: str, node_v: str):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()


class GraphBuilderDirector:
    @staticmethod
    def build_graph_from_csv(file_name: str, graph_builder: GraphBuilder, threshold: int):
        df = pd.read_csv(file_name)
        user_ids = df['user_id'].unique()
        user_business_rated: dict[str, set] = {}
        for user_id in tqdm(user_ids, desc='extracting business rated by each user'):
            user_business_rated[user_id] = set()
            user_entries = df[df['user_id'] == user_id]
            business_rated = user_entries['business_id']
            for business in business_rated:
                user_business_rated[user_id].add(business)
        for user_u in tqdm(user_business_rated.keys(), desc='building graph based on threshold'):
            for user_v in user_business_rated.keys():
                if user_v == user_u:
                    continue
                user_u_rated = user_business_rated[user_u]
                user_v_rated = user_business_rated[user_v]
                intersection = user_v_rated.intersection(user_u_rated)
                if len(intersection) >= threshold:
                    graph_builder.add_edge(user_u, user_v)


class SelfImplementedGraphBuilder(GraphBuilder):

    def __init__(self):
        self.graph = Graph()

    def add_edge(self, node_u: str, node_v: str):
        self.graph.add_edge(node_u, node_v)

    def reset(self):
        self.graph = Graph()

    def build(self) -> Graph:
        result = self.graph
        self.reset()
        return result


class NetworkXGraphBuilder(GraphBuilder):
    def __init__(self):
        self.graph = nx.Graph()

    def add_edge(self, node_u: str, node_v: str):
        self.graph.add_edge(node_u, node_v)

    def reset(self):
        self.graph = nx.Graph()

    def build(self) -> nx.Graph:
        result = self.graph
        self.reset()
        return result
