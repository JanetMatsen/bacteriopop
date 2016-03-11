import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import pylab
import seaborn as sns
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.sampledata.les_mis import data
import dynamic_mode_decomposition as dmd


def create_one_graph_using_networkx(adj, nodes, edge_treshhold):
    """
    This function create a graph using the adjacency matrix adj and
    list of nodes.

    :param adj: a numpy array representing the adjacency matrix
    :param nodes: a list representing the nodes in the graph
    :param edge_treshhold: the treshhold on the elements of adjacency matrix adj for that
                           pair to be consider as an edge
    :return: the graph in networkX format
    """
    # create and empty graph
    G = nx.Graph()
    # add edges to the graph
    N = len(nodes)
    for node1 in range(N):
        for node2 in range(N):
            if node1 == node2 or abs(adj[node1][node2]) >= edge_treshhold:
                G.add_edge(node1, node2)
                G[node1][node2]['weight'] = adj[node1][node2]
    return G


def create_all_graphs(mappings, nodes_list, edge_treshhold=1e-10):
    """
    This function trnasforms the adjacency matrix into the graph for all the instances
    """
    graphs = {}
    for key in mappings.keys():
        graphs[key] = create_one_graph_using_networkx(mappings[key], nodes_list[key], edge_treshhold)
    return graphs


def save_graph(graph,file_name):
    """
    This function save the graph into a file called file_name
    """
    # initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig


def reduce_adjacency_matrix(adj, nodes, edge_threshold):
    """
    This function removes some rows and columns of the adjacency matrix
    according to their correlation with other elements in the adjacency
    matrix and returns a new (smaller) numpy array for adjacency and the
    new list of nodes considered in the matrix.
    :param adj: adjacency matrix
    :param nodes: name of nodes (row and column names)
    :param edge_threshold: minimum magnitude to search for and include
    """
    n = len(nodes)
    print "number of nodes (rows/columns): {}".format(n)
    print "first few nodes: {}".format(nodes[0:5])
    new_nodes_index = []
    kept_nodes_names = []
    # todo: return the names of the reduced data's rows, columns instead of
    # the index.

    # loop over the nodes (which is both a row and column) and look for
    # interactions that have greater magnitude than the specified
    # edge_threshold
    for node1 in range(n):
        remove = True
        for node2 in range(n):
            # look for whether this pair has a significant interaction.
            if abs(adj[node1][node2]) > edge_threshold or \
                            abs(adj[node2][node1]) > edge_threshold:
                remove = False
        if not remove:
            new_nodes_index.append(node1)
            kept_nodes_names.append(nodes[node1])
    new_adj = np.zeros([len(new_nodes_index), len(new_nodes_index)])
    for i, node1 in enumerate(new_nodes_index):
        for j, node2 in enumerate(new_nodes_index):
            new_adj[i][j] = adj[node1][node2]
    return new_adj, kept_nodes_names


def reduce_all_adjacency_matrixes_in_dict(adjacency_dict, node_dict,
                                          edge_threshold):
    reduced_array_dict = {}
    reduced_node_dict = {}
    for key in adjacency_dict.keys():
        reduced_array_dict[key], reduced_node_dict[key] = \
            reduce_adjacency_matrix(adjacency_dict[key],
                                    node_dict[key],
                                    edge_threshold)
    return reduced_array_dict, reduced_node_dict


def generate_x_y(adj):
    """
    This function creates a meshgrid for the adjacecny matrix in x-y plane

    :param adj:
    """
    s = adj.shape
    x, y = np.meshgrid(np.arange(s[0]), np.arange(s[1]))
    return x.ravel(), y.ravel()


def heatmap(adj, nodes):
    """
    This function creates a heat map for the numpy array adj

    :param adj:
    :param nodes:
    """
    x, y = generate_x_y(adj)
    x_min = 0
    y_min = 0
    x_max = len(nodes)-1
    y_max = len(nodes)-1
    plt.figure()
    plt.hexbin(x, y, C=adj.ravel(), gridsize=len(nodes)/2, cmap=cm.jet,
               bins=None, mincnt=-100, extent=[x_min, x_max, y_min, y_max])


def adjacency_matrix_heatmap(Adj, nodes,figure_title, file_name):
    """
    This function creates heat maps for the adjacency matrix Adj
    and save it into the file_name
    The Adj is in numpy array format
    nodes is the list of nodes
    figure_title is a string represnting the tile of the saved figure
    """
    heatmap(Adj, nodes)
    cb = plt.colorbar()
    cb.set_label('abundance')
    plt.title(figure_title)
    plt.savefig(file_name, bbox_inches="tight")
    # plt.show()

def plot_all_adjacency_heatmaps(mappings_in_pandas):
    """
    plot and save the heat maps of the matrices given in pandas data frame
    """
    for key in mappings_in_pandas:
        file_name=str(key[0])+'_oxygen_week_'+str(key[1])+'.pdf'
        ax = plt.axes()
        hmp = sns.heatmap(mappings_in_pandas[key],ax=ax)
        ax.set_title(str(key[0])+' oxygen, week '+str(key[1]))
        hmp.figure.set_figwidth(10)
        hmp.figure.set_figheight(10)
        hmp.figure
        hmp.figure.savefig(file_name,bbox_inches='tight')
        plt.clf()

def plot_aggregated_adjacency_heatmaps(mappings_in_pandas, type='Mean'):
    """
    plot and save the heat maps of the matrices given in pandas data frame
    mappings_in_pandas: is dictionary that contains two elements, including
                        information for 'High' and 'Low' replicates
    type: the type of matrices to be plotted such as Mean, STD, SNR
    """
    for key in mappings_in_pandas:
        file_name=key+"_replicates_"+type+'.pdf'
        ax = plt.axes()
        hmp = sns.heatmap(mappings_in_pandas[key],ax=ax)
        ax.set_title(key+' replicates '+ type)
        hmp.figure.set_figwidth(10)
        hmp.figure.set_figheight(10)
        hmp.figure
        hmp.figure.savefig(file_name,bbox_inches='tight')
        plt.clf()


