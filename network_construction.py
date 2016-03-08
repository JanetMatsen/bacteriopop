import networkx as nx
import dynamic_mode_decomposition as dmd
import matplotlib.pyplot as plt
from matplotlib import pylab


def create_one_graph(Adj, nodes, edge_treshhold):
    # create and empty graph
    G = nx.Graph()
    # add edges to the graph
    N = len(nodes)
    for node1 in range(N):
        for node2 in range(N):
            if node1 == node2 or Adj[node1][node2] >= edge_treshhold:
                G.add_edge(node1, node2)
                G[node1][node2]['weight'] = Adj[node1][node2]
    return G


def create_all_graphs(mappings, nodes_list, edge_treshhold=1e-10):
    graphs = {}
    for key in mappings.keys():
        graphs[key] = create_one_graph(mappings[key], nodes_list[key], edge_treshhold)
    return graphs

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

# #Assuming that the graph g has nodes and edges entered
# mappings, nodes_list = dmd.find_fixed_adjacency_matrix(0,None,False)
# for key in mappings.keys():
#     Adj = mappings[key]
#     nodes = nodes_list[key]
#     g = create_one_graph(Adj,nodes,edge_treshhold=1e-10)
    # file_name="graph.pdf"
    # save_graph(g,file_name)