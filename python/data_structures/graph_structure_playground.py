import pytest

class Graph:
    
    def __init__(self):
        self.nodes = dict(set())
    
    def add(self, node_id, edges):
        for e in edges:
            if e not in self.nodes:
                self.nodes[e] = set()
        if node_id not in self.nodes:
            self.nodes[node_id] = set()
        self.nodes[node_id].update(edges)
    
    def remove_node(self, node_id):
        
        for n, edges in self.nodes.items():
            if node_id in edges:
                self.nodes[n].remove(node_id)
        del self.nodes[node_id]
    
    def remove_edge(self, node_id, edge_id):
        for n in self.nodes.keys():
            if n == node_id:
                self.nodes[n].remove(edge_id)
    
    
    def print(self):
        print("state of graph")
        print(self.nodes)
        
        
    def find_path(self, from_node, to_node):
        if from_node not in self.nodes or to_node not in self.nodes:
            return None
        
        def _find_path(n, path):
            
            for e in self.nodes[n]:
                if e == to_node:
                    return [e]
                else:
                    print(e)
                    found_path = _find_path(e, path)
                    if found_path != []:
                        found_path.append(e)
                        return found_path
            return path  
                        
        path =  _find_path(from_node, [])
        if len(path) == 0:
            return None
        else:
            path.append(from_node)
            return path
        
    def get(self):
        return self.nodes

        
def test_add():
    graph = Graph()
    graph.add(1, [2, 3])
    assert graph.get() == {1: set([2,3]), 2: set([]), 3: set([])}
    
def test_remove_node():
    graph = Graph()
    graph.add(1, [2, 3])
    graph.remove_node(2)
    assert graph.get() == {1: set([3]), 3: set()}
    
def test_remove_edge():
    graph = Graph()
    graph.add(1, [2, 3])
    graph.remove_edge(1, 2)
    assert graph.get() == {1: set([3]), 2: set(), 3: set()}
    
def test_find_path_no_from():
    graph = Graph()
    graph.add(2, [3, 4])
    graph.add(3, [4, 5])
    graph.add(4, [6])
    assert graph.find_path(1, 7) == None
    
def test_find_path_no_to():
    graph = Graph()
    graph.add(2, [3, 4])
    graph.add(3, [4, 5])
    graph.add(4, [6])
    assert graph.find_path(1, 7) == None
    
    
def test_path_not_found():
    graph = Graph()
    graph.add(1, [2, 3])
    graph.add(2, [3, 4])
    graph.add(3, [4, 5])
    graph.add(4, [6])
    graph.add(5, [7])
    assert graph.find_path(4, 7) == None

    

def test_find_path_backout():
    graph = Graph()
    graph.add(1, [2, 3])
    graph.add(2, [3, 4])
    graph.add(3, [4, 5])
    graph.add(4, [6])
    graph.add(5, [7])
    assert sorted(graph.find_path(1, 7)) == [1, 2, 3, 5, 7]

    
def test_find_path_simple_dfs():
    graph = Graph()
    graph.add(1, [2, 3])
    graph.add(2, [3, 4])
    graph.add(3, [4, 5])
    graph.add(4, [6])
    graph.add(5, [7])
    assert sorted(graph.find_path(1, 3)) == [1, 2, 3]
    

def test_find_path_1_6():
    graph = Graph()
    graph.add(1, [2, 3])
    graph.add(2, [3, 4])
    graph.add(3, [4, 5])
    graph.add(4, [6])
    graph.add(5, [7])
    assert sorted(graph.find_path(1, 6)) == [1, 2, 3, 4, 6]

    
pytest.main()
