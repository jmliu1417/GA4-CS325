'''
    This file contains the template for Assignment4.  For testing it, I will place it
    in a different directory, call the function <can_turn_off_lights>,
    and check its output. So, you can add/remove  whatever you want to/from this file.  But,
    don't change the name of the file or the name/signature of the following function.

    Also, I will use <python3> to run this code.
'''
from collections import defaultdict

# Parse the input file into instances
def parse_input(file_path):
    instances = []
    
    with open(file_path, 'r') as infile:
        lines = infile.readlines()
    
    current_instance = None
    
    for line in lines:
        line = line.strip()
        
        if line == "***":
            if current_instance is not None:
                instances.append(current_instance)
            current_instance = {
                'num_switches': 0,
                'num_lights': 0,
                'initial_state': [],
                'connections': []
            }
        elif current_instance is not None:
            if current_instance['num_switches'] == 0 and current_instance['num_lights'] == 0:
                # First line of the instance: number of switches and lights
                n, m = map(int, line.split(','))
                current_instance['num_switches'] = n
                current_instance['num_lights'] = m
            elif len(current_instance['initial_state']) == 0:
                # Second line of the instance: initial state of lights
                current_instance['initial_state'] = list(map(int, line.split(',')))
            else:
                # Following lines: connections for each switch
                current_instance['connections'].append(list(map(int, line.split(','))))
    
    if current_instance is not None:
        instances.append(current_instance)
    
    return instances

# Directed graph class for 2-SAT checking
class dir_graph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.nodes = set()

    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.nodes.add(u)
        self.nodes.add(v)

# Helper function to perform DFS
def DFS(dir_graph, visited, stack, scc):
    for node in dir_graph.nodes:
        if node not in visited:
            explore(dir_graph, visited, node, stack, scc)

# Explore a node in DFS
def explore(dir_graph, visited, node, stack, scc):
    if node not in visited:
        visited.append(node)
        for neighbour in dir_graph.graph[node]:
            explore(dir_graph, visited, neighbour, stack, scc)
        stack.append(node)
        scc.append(node)
    return visited

# Transpose the directed graph
def transpose_graph(d_graph):
    t_graph = dir_graph()
    for node in d_graph.graph:
        for neighbour in d_graph.graph[node]:
            t_graph.addEdge(neighbour, node)
    return t_graph

# Kosaraju's algorithm to find strongly connected components
def strongly_connected_components(dir_graph):
    stack = []
    sccs = []
    DFS(dir_graph, [], stack, [])
    t_g = transpose_graph(dir_graph)
    visited = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc = []
            scc.append(node)
            explore(t_g, visited, node, [], scc)
            sccs.append(scc)
    return sccs

# Check if there is a contradiction in the SCCs
def find_contradiction(sccs):
    for component in sccs:
        for literal in component:
            for other_literal in component[component.index(literal):]:
                if other_literal == "~" + literal:
                    return True
    return False

# Check if a given 2-CNF is satisfiable
def two_sat_solver(two_cnf_formula):
    graph = dir_graph()
    for clause in two_cnf_formula:
        u = clause[0]
        v = clause[1]
        graph.addEdge("~" + u, v)
        graph.addEdge("~" + v, u)
    
    sccs = strongly_connected_components(graph)
    return not find_contradiction(sccs)

# Convert the input data to 2-SAT format
def convert_to_2sat(instances):
    results = []
    
    for instance in instances:
        num_switches = instance['num_switches']
        num_lights = instance['num_lights']
        initial_state = instance['initial_state']
        connections = instance['connections']
        
        # Create a 2-CNF formula based on the initial state of the lights
        two_cnf_formula = []
        
        # We need to ensure that if the light is ON, we can turn it OFF, and vice versa
        for j in range(num_lights):
            if initial_state[j] == 1:  # Light L_j is ON
                connected_switches = []
                for i in range(num_switches):
                    if (j + 1) in connections[i]:  # +1 because lights are 1-indexed
                        connected_switches.append(f"S_{i + 1}")
                
                if connected_switches:
                    # To turn the light off, at least one of the connected switches should be ON
                    two_cnf_formula.append([f"~S_{i + 1}", f"L_{j + 1}"])  # Need to turn off L_j
            else:  # Light L_j is OFF
                connected_switches = []
                for i in range(num_switches):
                    if (j + 1) in connections[i]:
                        connected_switches.append(f"S_{i + 1}")
                
                if connected_switches:
                    # For OFF lights, we need to make sure they stay OFF
                    two_cnf_formula.append([f"S_{i + 1}", f"~L_{j + 1}"])  # Make sure L_j stays OFF

        # Check if the 2-CNF formula is satisfiable
        if two_sat_solver(two_cnf_formula):
            results.append("yes")
        else:
            results.append("no")
    
    return results


# Function to process input and output
def can_turn_off_lights(input_file_path, output_file_path):
    instances = parse_input(input_file_path)
    results = convert_to_2sat(instances)
    
    with open(output_file_path, 'w') as outfile:
        for result in results:
            outfile.write(result + "\n")


'''
    To test your function, you can uncomment the following command with the the input/output
    files paths that you want to read from/write to.
'''

can_turn_off_lights('inputs/input3.txt', 'output.txt')