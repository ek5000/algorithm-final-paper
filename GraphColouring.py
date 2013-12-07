import fileinput

__author__ = 'ek'
import networkx as nx
from networkx import *

numberOfNodes = 50


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
        for j in range(0, i):
            inner_node = list_of_nodes[j]
            try:
                edge = graph.edge[outer_node][inner_node]
                if graph.node[outer_node]['color'] == graph.node[inner_node]['color']:  # edge existed, and was the same color
                    graph.node[outer_node]['color'] = -1
            except:  # No edge between the i and j, check if color should be assigned
                if graph.node[outer_node]['color'] >= graph.node[inner_node]['color'] or graph.node[outer_node]['color'] == -1: # Either a possible lower color or  no color assigned
                    graph.node[outer_node]['color'] = graph.node[inner_node]['color']
        if graph.node[outer_node]['color'] == -1: ## Create a new color
            newColor = len(colorsUsed)
            graph.node[outer_node]['color'] = newColor
            colorsUsed.append(newColor)

    return colorsUsed

def order_nodes_by_degree(graph):
    nodes_with_degreess = list(graph.degree_iter())
    sorted_list_of_nodes = sorted(nodes_with_degreess, key=lambda node: -node[1])
    list_of_nodes = []
    for node_pair in sorted_list_of_nodes:
        list_of_nodes.append(node_pair[0])

    return list_of_nodes

def main():
    graph = read_graph_from_adjacent_matrix(fileinput.input())
    list_of_nodes = order_nodes_by_degree(graph)

    colorsUsed = greedy_vertex_coloring(graph, list_of_nodes)

    print(colorsUsed)


if __name__ == '__main__':
    main()