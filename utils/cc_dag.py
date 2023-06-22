import networkx as nx
from itertools import product
import copy
import matplotlib.pyplot as plt

class DAG:

    def __init__(self):
        self.g = nx.DiGraph()
        self.equalities = []
        self.inequalities = []

    def __str__(self):
        result = ""
        for node in self.g.nodes:
            node_string = self.node_string(node)
            result += f"{node} {node_string}\n"
        return result

    def add_node(self,id,fn,args):
        mutable_ccpar = set()
        self.g.add_node(id,fn=fn, args=args, mutable_find=id,mutable_ccpar=mutable_ccpar)

    # PRINT NODE
    def node_string(self,id):
        target = self.g.nodes[id]
        if not target["args"]: #if it's a constant it returns only the fn (e.g. a or b)
            return str(target["fn"])
        else:
            args_str = ", ".join(self.node_string(arg) for arg in target["args"]) #recursively to rapresent something like f(f(a,b),b)
            return f"{target['fn']}({args_str})"

    def get_fn(self,id):
        target = self.g.nodes[id]
        return target["fn"]
    def get_node(self,id):
        return self.g.nodes[id]

    def complete_ccpar(self):
        for id in self.g.nodes:
            self.add_father(id)
            pass

    def add_father(self,id):
        father_args = self.g.nodes[id]["args"]
        for arg in father_args:
            self.g.nodes[arg]["mutable_ccpar"].add(id)

    def find(self,id):
        #takes a node_id and returns the node representative of the class of the first node
        node = self.g.nodes[id]
        if node["mutable_find"] == id:
            return id
        else:
            return self.find(node["mutable_find"]) #recursive function

    def ccpar(self,id):
        result = self.g.nodes[self.find(id)] #restituisce il ccpar del nodo rappresentativo della classe
        return result["mutable_ccpar"]

    def union(self,id1,id2):
        node1 = self.g.nodes[self.find(id1)]
        node2 = self.g.nodes[self.find(id2)]
        if len(node2["mutable_ccpar"])> len(node1["mutable_ccpar"]):#to implement the point 2 of the optional in the project.pdf
            node1["mutable_find"]  = copy.copy(node2["mutable_find"])
            node2["mutable_ccpar"].update(node1["mutable_ccpar"])
            node1["mutable_ccpar"] = set()
        else:
            node2["mutable_find"]  = copy.copy(node1["mutable_find"])
            node1["mutable_ccpar"].update(node2["mutable_ccpar"])
            node2["mutable_ccpar"] = set()

    def congruent(self,id1,id2):
        node1 = self.g.nodes[id1]
        node2 = self.g.nodes[id2]
        if not(node1["fn"] == node2["fn"]):
            return False
        if len(node1["args"]) != len(node2["args"]):
            return False #optional
        for a1, a2 in zip(node1["args"], node2["args"]):
            if self.find(a1) != self.find(a2):
                return False
        return True

    def merge(self,id1,id2):
        repr1 = self.find(id1)
        repr2 = self.find(id2)
        if repr1!=repr2:
            ccpar1 = self.ccpar(id1)
            ccpar2 = self.ccpar(id2)
            self.union(id1,id2)
            for t1,t2 in product(ccpar1,ccpar2):
                if (self.find(t1) != self.find(t2)) and self.congruent(t1,t2):
                    self.merge(t1,t2)#recursive
            return True
        else:
            return False


    def solve(self):
        for eq in self.equalities:
            if (eq in self.inequalities) or (eq[::-1] in self.inequalities): #implement forbidden list
                return "UNSAT (from Forbidden List)"
            val1,val2 =  self.find(eq[0]),self.find(eq[1])
            self.merge(eq[0],eq[1])
        for ineq in self.inequalities:
            val1,val2 =  self.find(ineq[0]),self.find(ineq[1])
            if val1 == val2: # If the inequality is not correct it's UNSAT
                return "UNSAT"
        return "SAT"

    def print_graph(self):
        # Create a new graph
        graph = nx.DiGraph()
        labels = {node: f"id: {node}, fn: {self.get_fn(node)}"  for node in self.g.nodes}
        for node in self.g.nodes:
            graph.add_node(node)
        for node in self.g.nodes:
            for par in self.ccpar(node):
                if not(par == node):
                    graph.add_edge(par, node)
        pos = nx.spring_layout(graph)

        # Draw the graph
        nx.draw(graph,pos, with_labels = True, labels = labels ,node_size = 500, node_color = "red", font_size = 10, font_color = "black", edge_color = "gray", arrows = True)
        # Display the graph
        plt.show()
        return graph

    def print_graph_solved(self, graph):
        new_edges = []
        labels = {node: f"id: {node}, fn: {self.get_fn(node)}"  for node in self.g.nodes}
        for node in self.g.nodes:
            if not(node == self.find(node)):
                new_edges.append((self.find(node), node))
        pos = nx.spring_layout(graph)
        nx.draw_networkx_edges(graph, pos, edgelist= new_edges, style = 'dotted',connectionstyle='arc3 ,rad=0.3')
        nx.draw(graph,pos, with_labels = True, labels = labels ,node_size = 500, node_color = "red", font_size = 10, font_color = "black", edge_color = "gray", arrows = True)
        plt.show()