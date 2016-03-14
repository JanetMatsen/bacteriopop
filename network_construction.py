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


def aggregate_adjacency_matrices(list_of_dfs):
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
    # Separate the high and low oxygen results before aggregating.
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


def plot_heatmap(dataframe, title, file_name, filetype='pdf',
                 width=10, height=10):
        ax = plt.axes()
        hmp = sns.heatmap(dataframe, ax=ax)
        ax.set_title(title)
        hmp.figure.set_figwidth(width)
        hmp.figure.set_figheight(height)
        hmp.figure
        hmp.figure.savefig(file_name, bbox_inches='tight')
        plt.clf()


def plot_all_adjacency_heatmaps(mappings_in_pandas):
    """
    plot and save the heat maps of the matrices given in pandas data frame
    :param mappings_in_pandas:
    """
    for key in mappings_in_pandas:
        file_name = 'plots/' + str(key[0]) + '_oxygen_week_' + \
                    str(key[1])
        title = str(key[0])+' oxygen, week '+str(key[1])
        plot_heatmap(mappings_in_pandas[key], title, file_name)
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
