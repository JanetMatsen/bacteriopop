import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import pylab
import pandas as pd
import seaborn as sns


def create_one_graph_using_networkx(adj, nodes, edge_threshold):
    """
    This function create a graph using the adjacency matrix adj and
    list of nodes.

    :param adj: a numpy array representing the adjacency matrix
    :param nodes: a list representing the nodes in the graph
    :param edge_threshold: the threshold on the elements of adjacency
    matrix adj for that pair to be consider as an edge
    :return: the graph in networkX format
    """
    # create and empty graph
    g = nx.Graph()
    # add edges to the graph
    n = len(nodes)
    for node1 in range(n):
        for node2 in range(n):
            if node1 == node2 or abs(adj[node1][node2]) >= edge_threshold:
                g.add_edge(node1, node2)
                g[node1][node2]['weight'] = adj[node1][node2]
    return g


def create_all_graphs(mappings, nodes_list, edge_threshold=1e-10):
    """
    Transforms the adjacency matrix into the graph for all the instances
    :param mappings:
    :param nodes_list:
    :param edge_threshold:
    """
    graphs = {}
    for key in mappings.keys():
        graphs[key] = create_one_graph_using_networkx(mappings[key],
                                                      nodes_list[key],
                                                      edge_threshold)
    return graphs


def save_graph(graph, file_name):
    """
    This function saves the graph into a file called file_name
    :param graph:
    :param file_name:
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

    plt.savefig('plots/' + file_name, bbox_inches="tight")
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
    """
    This function iterate over all replicates in the adjacency_dict
    which include 4 high O2 and 4 low O2 samples and applies the
    construct a new adjacency matrix based on the edge_treshold.
    edge_treshhold represents the minimum amount of interaction
    between bacteria needed to be considered as an edge in the
    network of bacteria.
    """
    reduced_array_dict = {}
    reduced_node_dict = {}
    for key in adjacency_dict.keys():
        reduced_array_dict[key], reduced_node_dict[key] = \
            reduce_adjacency_matrix(adjacency_dict[key],
                                    node_dict[key],
                                    edge_threshold)
    return reduced_array_dict, reduced_node_dict


def aggregate_adjacency_matrices(list_of_dfs):
    """
    This function take the list of all adjacency matrices found for each high/low
    replicate and calculate the mean, standard deviation and signal to noise ratio
    over the 4 replicates in high/low groups.
    """
    # Generalized aggregator.  Will write a wrapper that individually makes
    # one for each High/Low O2 condition.
    # Returns yet another dictionary!  (ha ha)

    # Use Pandas panel to gather the replicates, and to make summary
    # dataframes of the element-by-element averages, standard deviations,
    # and signal-to-noise.
    # Note that we are using 0, 1, 2... for keys in the Panel object.  We
    # could use the descriptive tuples, but there is currently no advantage.
    p = pd.Panel(data={n: df for n, df in enumerate(list_of_dfs)})
    # Use this Panel object to make summary statistics.
    summary_df_dict = {}
    summary_df_dict['mean'] = p.mean(axis=0)
    summary_df_dict['standard deviation'] = p.std(axis=0)
    # to get signal to noise, we need to make a panel of these new dataframes.
    p2 = pd.Panel(data={n: df for n, df in
                        enumerate([summary_df_dict['mean'],
                                  summary_df_dict['standard deviation']])})
    # todo: figure out how to use our own function to calculate signal to noise
    # summary_df_dict['signal to noise'] =
    return summary_df_dict


def summarize_replicate_adjacency_matrices(result_dict):
    """
    This function separates the high and low oxygen results before aggregating.
    The output is a dictionary of dictionaries.
    """
    high_oxygen_dfs = []
    low_oxygen_dfs = []
    # loop over the results dict.  The keys are tuples like ("Low",
    # 1) indicating their low/high oxygen content and replicate number.  Use
    #  the "Low" or "High" string to sort before aggregation.
    for oxy_rep_tuple in result_dict.keys():
        if oxy_rep_tuple[0] == "Low":
            low_oxygen_dfs.append(result_dict[oxy_rep_tuple])
        else:
            high_oxygen_dfs.append(result_dict[oxy_rep_tuple])
    # Now we can pass these lists of dataframes to
    # aggregate_adjacency_matrices(), which calculates the means and
    # standard deviations.  This will help us find the important and
    # reproducible correlations/effects.
    low_oxy_summary = aggregate_adjacency_matrices(low_oxygen_dfs)
    high_oxy_summary = aggregate_adjacency_matrices(high_oxygen_dfs)
    # create a dictionary to hold each dictionary.  Now we are wishing we
    # had classes!
    return {"Low": low_oxy_summary, "high": high_oxy_summary}


def plot_heatmap(dataframe, title=None, file_name=None, file_type='pdf',
                 width=10, height=10):
    """
    Plot a heat map of any data frame.

    :param dataframe: data to plot as a heat map
    :param title: optional title
    :param file_name: optional filename
    :param filetype: optional filetype
    :param width: figure width (inches)
    :param height: figue height (inches)
    :return: a seaborn heat map, whic was saved if file_name was provided.
    """
    ax = plt.axes()
    # generate a seaborn heatmap on the axis ax
    hmp = sns.heatmap(dataframe, ax=ax)
    # add a title if it was passed to the function
    if title:
        ax.set_title(title)
    # adjust the figure size
    hmp.figure.set_figwidth(width)
    hmp.figure.set_figheight(height)
    if file_name:
        hmp.figure.savefig(file_name + file_type, bbox_inches='tight')
    return hmp


def o2_rep_tuple_to_string(o2_rep_tuple):
    """
    this function create a string description for a sample
    called o2_rep_tuple
    """
    return str(o2_rep_tuple[0]) + '_oxygen_week_' + str(o2_rep_tuple[1])


def plot_all_adjacency_heatmaps(mappings_in_pandas):
    """
    plot and save the heat maps of the matrices given in pandas data frame
    :param mappings_in_pandas:
    """
    for key in mappings_in_pandas:
        file_name = 'plots/' + o2_rep_tuple_to_string(key)
        title = str(key[0])+' oxygen, week '+str(key[1])
        plot_heatmap(mappings_in_pandas[key], title, file_name,
                     file_type='.pdf')
        plt.clf()


def plot_aggregated_adjacency_heatmaps(mappings_in_pandas, dtype='Mean'):
    """
    plot and save the heat maps of the matrices given in pandas data frame
    :param mappings_in_pandas: a dictionary that containing two elements,
    including information for 'High' and 'Low' replicates
    :param dtype: the type of matrices to be plotted such as Mean, STD, SNR
    """
    # Todo: simplify by using plot_heatmap()
    for key in mappings_in_pandas:
        file_name = 'plots/'+key+"_oxygen_replicates_" + dtype
        ax = plt.axes()
        hmp = sns.heatmap(mappings_in_pandas[key], ax=ax)
        ax.set_title(key + ' oxygen replicates ' + dtype)
        hmp.figure.set_figwidth(10)
        hmp.figure.set_figheight(10)
        hmp.figure
        hmp.figure.savefig(file_name, bbox_inches='tight')
        plt.clf()
