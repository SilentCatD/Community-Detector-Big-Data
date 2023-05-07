from graph_builder import SelfImplementedGraphBuilder, NetworkXGraphBuilder, GraphBuilderDirector
from betweenness_calculator import BetweennessCalculator, NetworkXBetweennessCalculator, \
    SelfImplementedBetweennessCalculator
from community_detector import CommunityDetector, NetworkxCommunityDetector, SelfImplementedCommunityDetector

if __name__ == '__main__':
    # set metadata
    threshold = 7
    data_file = 'data/ub_sample_data.csv'

    # ==================================================

    # build graph

    # self implemented_graph
    implemented_graph_builder = SelfImplementedGraphBuilder()
    GraphBuilderDirector.build_graph_from_csv(data_file, implemented_graph_builder, threshold)
    implemented_graph = implemented_graph_builder.build()

    # networkx graph
    networkx_graph_builder = NetworkXGraphBuilder()
    GraphBuilderDirector.build_graph_from_csv(data_file, networkx_graph_builder, threshold)
    networkx_graph = networkx_graph_builder.build()

    # ==================================================

    # betweenness calculation
    betweenness_out_file = 'output/edge_betweenness.txt'
    betweenness_lib_out_file = 'output/edge_betweenness_lib.txt'

    # betweenness self implemented
    implemented_betweenness_calculator = SelfImplementedBetweennessCalculator(implemented_graph)
    implemented_edge_betweenness = implemented_betweenness_calculator.calculate_betweenness(betweenness_out_file)

    # betweenness lib
    lib_edge_betweenness_calculator = NetworkXBetweennessCalculator(networkx_graph)
    edges_betweenness_lib = lib_edge_betweenness_calculator.calculate_betweenness(betweenness_lib_out_file)

    # benchmark betweenness
    BetweennessCalculator.mse_benchmark_betweenness(betweenness_out_file, betweenness_lib_out_file)

    # ==================================================

    # community detection

    community_detection_out_file = 'output/communities.txt'
    community_detection_lib_out_file = 'output/communities_lib.txt'

    # detection self implemented
    community_detector = SelfImplementedCommunityDetector(implemented_graph)
    community_detector.detect(community_detection_out_file)

    # detection networkx
    community_detector_lib = NetworkxCommunityDetector(networkx_graph)
    community_detector_lib.detect(community_detection_lib_out_file)

    # benchmark communities
    CommunityDetector.benchmark_communities(community_detection_out_file, community_detection_lib_out_file)
