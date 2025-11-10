import networkx as nx
import matplotlib.pyplot as plt
import heapq
from typing import List, Tuple

class CampusNetwork:
    def __init__(self):
        self.graph = nx.Graph()
        self.buildings = {}
        self.mst = None
        
    def add_building(self, name: str, x: float, y: float):
        self.buildings[name] = (x, y)
        self.graph.add_node(name, pos=(x, y))
    
    def add_connection(self, building1: str, building2: str, cost: float):
        if building1 in self.buildings and building2 in self.buildings:
            self.graph.add_edge(building1, building2, weight=cost)
    
    def kruskal_mst(self) -> nx.Graph:
        edges = sorted(self.graph.edges(data=True), key=lambda x: x[2]['weight'])
        mst = nx.Graph()
        parent = {node: node for node in self.graph.nodes()}
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]
        
        def union(node1, node2):
            root1, root2 = find(node1), find(node2)
            if root1 != root2:
                parent[root2] = root1
                return True
            return False
        
        total_cost = 0
        for node in self.graph.nodes():
            mst.add_node(node, pos=self.buildings[node])
            
        for u, v, data in edges:
            if union(u, v):
                mst.add_edge(u, v, weight=data['weight'])
                total_cost += data['weight']
        
        self.mst = mst
        print(f"Kruskal's MST Total Cost: ${total_cost:,.2f}")
        return mst
    
    def prim_mst(self) -> nx.Graph:
        if not self.graph.nodes():
            return nx.Graph()
        
        mst = nx.Graph()
        visited = set()
        start_node = list(self.graph.nodes())[0]
        pq = [(0, start_node, None)]
        total_cost = 0
        
        while pq and len(visited) < len(self.graph.nodes()):
            weight, current, previous = heapq.heappop(pq)
            if current in visited:
                continue
                
            visited.add(current)
            mst.add_node(current, pos=self.buildings[current])
            if previous is not None:
                mst.add_edge(previous, current, weight=weight)
                total_cost += weight
            
            for neighbor, data in self.graph[current].items():
                if neighbor not in visited:
                    heapq.heappush(pq, (data['weight'], neighbor, current))
        
        self.mst = mst
        print(f"Prim's MST Total Cost: ${total_cost:,.2f}")
        return mst
    
    def visualize_network(self, show_mst: bool = False, highlight_path: List[str] = None):
        plt.figure(figsize=(12, 8))
        graph_to_show = self.mst if show_mst else self.graph
        pos = nx.get_node_attributes(graph_to_show, 'pos')
        
        nx.draw_networkx_nodes(graph_to_show, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_labels(graph_to_show, pos, font_size=8, font_weight='bold')
        
        edge_labels = nx.get_edge_attributes(graph_to_show, 'weight')
        nx.draw_networkx_edges(graph_to_show, pos, alpha=0.7, edge_color='gray')
        nx.draw_networkx_edge_labels(graph_to_show, pos, edge_labels=edge_labels)
        
        if highlight_path:
            path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
            nx.draw_networkx_edges(graph_to_show, pos, edgelist=path_edges, 
                                  edge_color='red', width=3, alpha=0.8)
            nx.draw_networkx_nodes(graph_to_show, pos, nodelist=highlight_path, 
                                  node_color='red', node_size=600)
        
        plt.title(f"Campus Network {'(MST)' if show_mst else ''}")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def create_sample_campus():
    campus = CampusNetwork()
    buildings = [
        ("Library", 2, 8), ("Admin", 5, 9), ("Science", 8, 7), 
        ("Engineering", 6, 5), ("Arts", 3, 6), ("Student Center", 1, 4),
        ("Dorm A", 4, 2), ("Dorm B", 7, 3), ("Gym", 9, 1), ("Cafeteria", 5, 1)
    ]
    for name, x, y in buildings:
        campus.add_building(name, x, y)
    
    connections = [
        ("Library", "Admin", 50000), ("Library", "Arts", 35000),
        ("Admin", "Science", 60000), ("Admin", "Engineering", 45000),
        ("Science", "Engineering", 30000), ("Science", "Gym", 80000),
        ("Engineering", "Arts", 40000), ("Engineering", "Dorm B", 55000),
        ("Arts", "Student Center", 25000), ("Student Center", "Dorm A", 20000),
        ("Dorm A", "Dorm B", 35000), ("Dorm A", "Cafeteria", 15000),
        ("Dorm B", "Gym", 40000), ("Dorm B", "Cafeteria", 30000),
        ("Gym", "Cafeteria", 50000)
    ]
    for b1, b2, cost in connections:
        campus.add_connection(b1, b2, cost)
    
    return campus

if __name__ == "__main__":
    campus = create_sample_campus()
    
    print("1. Original Network")
    campus.visualize_network(show_mst=False)
    
    print("2. Kruskal's MST")
    campus.kruskal_mst()
    campus.visualize_network(show_mst=True)
    
    print("3. Prim's MST")
    campus.prim_mst()
    campus.visualize_network(show_mst=True)