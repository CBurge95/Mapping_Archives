import csv
import networkx as nx
from operator import itemgetter
import community

with open('1523-1540_data.csv','r') as edgescsv: #edgelist
	edgereader = csv.reader(edgescsv) 
	edges = [tuple(e) for e in edgereader][1:] 
	
with open('full_person_list.csv','r') as nodescsv: #nodelist
	nodereader = csv.reader(nodescsv)
	nodes = [n for n in nodereader][1:]
node_names = [n[0] for n in nodes]

MG = nx.MultiDiGraph()
MG.add_edges_from(edges)
G = nx.DiGraph()
for u,v,data in MG.edges(data=True):
	w = data['weight'] if 'weight' in data else 1.0
	if G.has_edge(u,v):
			G[u][v]['weight'] += w
	else:
			G.add_edge(u, v, weight=w)	

hist_name_dict = {}
for node in nodes:
	hist_name_dict[node[0]] = node[1]	
nx.set_node_attributes(G, hist_name_dict, 'historical_name')

Gund = nx.to_undirected(G)

def archive_set(node):
	archive = set(Gund.neighbors(node))
	archive.add(node)
	edges = G.edges(node)
	return archive, edges

TC_archives, TC_edges = archive_set('32545')
Lisle_archives, Lisle_edges = archive_set('1683')
Henry_archives, Henry_edges = archive_set('11844')
Wolsey_archives, Wolsey_edges = archive_set('3674')
Lady_archives, Lady_edges = archive_set('12118')

All_Edges, All_Nodes = {}, {}
for edge in list(G.edges()):
	All_Edges[edge] = '1'
for node in G:
	All_Nodes[node] = '1'

def EdgeLabel(archive, item):
	for u,v in All_Edges.items():
		if u in archive:
			if v == '1':
				All_Edges[u] = item
			if v != '1':
				All_Edges[u] = str(v + ", " + item)
	return
def NodeLabel(archive, item):
	for u, v in All_Nodes.items():
		if u in archive:
			if v == '1':
				All_Nodes[u] = item
			if v != '1':
				All_Nodes[u] = str(v + ", " + item)
	return

NodeLabel(TC_archives, 'Cromwell')
NodeLabel(Lisle_archives, 'Lord Lisle')
NodeLabel(Henry_archives, 'Henry')
NodeLabel(Wolsey_archives, 'Wolsey')
NodeLabel(Lady_archives, 'Lady Lisle')
EdgeLabel(TC_edges, 'Cromwell')
EdgeLabel(Lisle_edges, 'Lord Lisle')
EdgeLabel(Henry_edges, 'Henry')
EdgeLabel(Wolsey_edges, 'Wolsey')
EdgeLabel(Lady_edges, 'Lady Lisle')
			
nx.set_edge_attributes(G, All_Edges, 'Archive')
nx.set_node_attributes(G, All_Nodes, 'Archive')

sublibrary = []
for node in G:
	if G.degree(node) >= 1:
		sublibrary.append(node)
		
subgraph = G.subgraph(sublibrary)		

	
nx.write_gexf(subgraph,'Venn_Archives_23-40_2.gexf')
