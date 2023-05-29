from Gates import generate_output
from pysat.solvers import Solver


class Node:
    def __init__(self,kind, name, num_inputs, inputs_names, output):
        self.kind = kind
        self.name = name
        self.inputs_names = inputs_names
        self.num_inputs = int(num_inputs)
        self.inputs_val = []
        self.original_inputs_val = []
        self.output_name = output
        self.output_val = -1
        self.flip = False

    def to_flip(self):
        if self.flip:
            self.flip = False
        else:
            self.flip = True

    def reset_flip(self):
        self.flip = False



class Edge:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def __init__(self, content, gates):
        self.nodes = {}
        self.edges = []
        for line in content:
            kind = line[0]
            name = line[1]
            output = line[2]
            inputs = line[3: len(line)]
            self.add_node(kind, name, inputs, output)


        # generate edges
        for src in content:
            output = src[2]
            for dst in content:
                dst_inputs = dst[3: len(dst)]
                if output in dst_inputs:
                    self.add_edge(src[1], dst[1])

    def add_node(self, kind, name, inputs, output):
        node = Node(kind, name, len(inputs), inputs, output)
        self.nodes[name] = node

    def add_edge(self, source, dest):
        edge = Edge(source, dest)
        self.edges.append(edge)

    def print_graph(self):
        print("Nodes:")
        for name, node in self.nodes.items():
            inputs_str = ", ".join(str(i) for i in node.inputs_names)
            inputs_val_str = ", ".join(str(i) for i in node.inputs_val)
            org_inputs_val_str = ", ".join(str(i) for i in node.original_inputs_val)
            print(
                f"{name}: num_inputs={node.num_inputs}, inputs=[{inputs_str}], inputs_val=[{inputs_val_str}], org_inputs_val_str=[{org_inputs_val_str}], output_name= {node.output_name}, output_val= {node.output_val}, flip={node.flip}")

        print("\nEdges:")
        for edge in self.edges:
            print(f"{edge.source} -> {edge.dest}")

    def flip(self, name):
        node = self.nodes.get(name)
        node.to_flip()

    def setBack(self):  # set all flip to false, and all num_inputs
        for node in self.nodes.values():
            node.reset_flip()
            node.inputs_val = node.original_inputs_val.copy()
            node.output_val = -1

    def generate_output(self, gates, par_val, input_gates):
        for gate in gates:
            self.flip(gate)
        while(True):
            node = self.next_node() #give a node that all his inputs are "feed" and has no output yet
            if node == None:
                break
            generate_output(node)
            output_name = node.output_name
            output_val = node.output_val
            self.generate_inputs(output_name, output_val)

    def next_node(self):
        for node in self.nodes.values():
            if (node.output_val == -1) and (len(node.inputs_val) == node.num_inputs): #if i have all the inputs provided but didnt calculate the output
                return node
        return None

    def generate_inputs(self, output_name, output_val):
        for node in self.nodes.values():
            if output_name in node.inputs_names:
                node.inputs_val.append(output_val)

    def generate_Original_inputs(self, output_name, output_val):
        for node in self.nodes.values():
            if output_name in node.inputs_names:
                node.inputs_val.append(output_val)
                node.original_inputs_val.append(output_val)

    def set_beforeTest(self):
        for node in self.nodes.values():
            node.original_inputs_val = []
            node.inputs_val = []

