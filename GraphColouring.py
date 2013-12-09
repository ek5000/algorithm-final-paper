import fileinput
import timeit
import time

__author__ = 'ek'
import networkx as nx
from networkx import *

numberOfNodes = 50

def read_multiple_graphs_from_adjacency_matrices(lines):
    graphs = []
    graph = nx.Graph()
    graphs.append(graph)
    graph.add_nodes_from(range(0, numberOfNodes), color=-1)
    index = 0
    for line in lines:
        if line == '-\n':
            index = 0
            graphs.append(graph)
            graph = nx.Graph()
            graph.add_nodes_from(range(0, numberOfNodes), color=-1)
            continue
        values = line.strip().split(' ')
        for i in range(0, numberOfNodes):
            if values[i] == '1':
                graph.add_edge(index, i)
        index += 1
    return graphs

def read_graph_from_adjacent_matrix(lines):
    graph = nx.Graph()
    graph.add_nodes_from(range(0, numberOfNodes), color=-1)
    index = 0
    for line in lines:
        values = line.strip().split(' ')
        for i in range(0, numberOfNodes):
            if values[i] == '1':
                graph.add_edge(index, i)
        index += 1
    return graph

def greedy_vertex_coloring(graph, list_of_nodes):
    colorsUsed = []
    for i in range(0, numberOfNodes):
        outer_node = list_of_nodes[i]
        visited_colors = [graph.node[x]['color'] for x in list_of_nodes[:i]]
        neighboring_colors = [graph.node[x]['color'] for x in graph.neighbors(outer_node)]
        possible_colors = list(set(visited_colors) - set(neighboring_colors))
        graph.node[outer_node]['color'] = i if not possible_colors else possible_colors[0]
        colorsUsed.append(i if not possible_colors else possible_colors[0])

    return list(set(colorsUsed))

def order_nodes_by_degree(graph):
    nodes_with_degreess = list(graph.degree_iter())
    sorted_list_of_nodes = sorted(nodes_with_degreess, key=lambda node: -node[1])
    list_of_nodes = []
    for node_pair in sorted_list_of_nodes:
        list_of_nodes.append(node_pair[0])

    return list_of_nodes

def check_validity_of_coloring(graph):
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            if graph.node[node]['color'] == graph.node[neighbor]['color']:
                print("Node was " + str(node) + "-" + str(graph.node[node]['color']) + ": Neighbor was " + str(neighbor) + "-" + str(graph.node[neighbor]['color']) + "")
                return False
    return True

def run_time_trials(graphs, method_to_order_by=lambda graph: order_nodes_by_degree(graph), outstream = sys.stdout):
    avg_number_of_colors = 0
    avg_time = 0
    for graph in graphs:
        start = time.time()
        list_of_nodes = method_to_order_by(graph)
        num_colors = len(greedy_vertex_coloring(graph, list_of_nodes))
        elapsed = time.time() - start
        if check_validity_of_coloring(graph) is False:
            raise Exception("Color produced wasn't valid")
        avg_number_of_colors += num_colors
        avg_time += elapsed
    ## normalize
    avg_number_of_colors /= len(graphs)
    avg_time /= len(graphs)
    outstream.write("Avg. Number of Colors: " + str(avg_number_of_colors) + "\n")
    outstream.write("Average Time Taken: " + str(avg_time) + "\n")
    outstream.write("Maximum Clique Size: " + str(nx.graph_clique_number(graph)))


def main():
    # Run a single graph
    # graph = read_graph_from_adjacent_matrix(fileinput.input())
    # list_of_nodes = order_nodes_by_degree(graph)
    # colorsUsed = greedy_vertex_coloring(graph, list_of_nodes)
    # check_validity_of_coloring(graph)

    ## Run multiple grahs
    graphs = read_multiple_graphs_from_adjacency_matrices(fileinput.input())
    run_time_trials(graphs, order_nodes_by_degree)


if __name__ == '__main__':
    main()