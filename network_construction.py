import networkx as nx


def create_one_graph(Adj, nodes, edge_treshhold):
    # create and empty graph
    G = nx.Graph()
    # add edges to the graph
    N = len(nodes)
    for node1 in range(N):
        for node2 in range(N):
            if node1 == node2 or Adj[node1, node2] >= edge_treshhold:
                G.add_edge(node1, node2)
    return G


def create_all_graphs(mappings, nodes_list, edge_treshhold=1e-10):
    graphs = {}
    for key in mappings.keys():
        graphs[key] = create_one_graph(mappings[key], nodes_list[key], edge_treshhold)
    return graphs

