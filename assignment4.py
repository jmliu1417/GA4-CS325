'''
    This file contains the template for Assignment4.  For testing it, I will place it
    in a different directory, call the function <can_turn_off_lights>,
    and check its output. So, you can add/remove  whatever you want to/from this file.  But,
    don't change the name of the file or the name/signature of the following function.

    Also, I will use <python3> to run this code.
'''
from collections import defaultdict

#parsing inputs into an instance dictionary or class format
def parse_input(file_path):
    instances = []
    
    with open(file_path, 'r') as infile:
        lines = infile.readlines()
    
    current_instance = None
    
    for line in lines:
        line = line.strip()
        
        if line == "***":
            # If we were already processing an instance, save it
            if current_instance is not None:
                instances.append(current_instance)
            # Start a new instance
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
    
    # Don't forget to add the last instance if it exists
    if current_instance is not None:
        instances.append(current_instance)
    
    return instances

# file_path = 'inputs/input1.txt'  # Adjust the path as necessary
# instances = parse_input(file_path)

# # Print the parsed instances for verification
# for i, instance in enumerate(instances):
#     print(f"Instance {i + 1}:")
#     print(f"  Number of Switches: {instance['num_switches']}")
#     print(f"  Number of Lights: {instance['num_lights']}")
#     print(f"  Initial State: {instance['initial_state']}")
#     print(f"  Connections: {instance['connections']}")

class Formula:
    def __init__(self):
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)

    def __str__(self):
        return '\n'.join([' '.join(clause) for clause in self.clauses])

def convert_to_2sat(instances):
    formula = Formula()
    
    for instance in instances:
        num_switches = instance['num_switches']
        num_lights = instance['num_lights']
        initial_state = instance['initial_state']
        connections = instance['connections']
        
        # Create clauses based on the initial state of the lights
        for j in range(num_lights):
            if initial_state[j] == 1:  # Light L_j is ON
                # We need at least one switch connected to L_j to be ON
                connected_switches = []
                for i in range(num_switches):
                    if (j + 1) in connections[i]:  # +1 because lights are 1-indexed
                        connected_switches.append(f'S_{i + 1}')  # Switches are also 1-indexed
                
                # Create the clause: (S_i1 OR S_i2 OR ... OR S_ik) => ~L_j
                if connected_switches:
                    # We can create a clause for each switch
                    for switch in connected_switches:
                        formula.add_clause([switch, f'~L_{j + 1}'])  # S_i OR ~L_j

    return formula

# Example usage
file_path = 'inputs/input1.txt'  # Adjust the path as necessary
instances = parse_input(file_path)  # Assuming parse_input function is defined

formula = convert_to_2sat(instances)

# Print the resulting clauses
print(formula)


# def convertor(input_file_path):
#     instances = parse_input(input_file_path)
    
#     m = {instances['num_switches']}
#     n = {instances['num_lights']}
#     initial_state = {instances['initial_state']}
#     connections = {instances['connections']}
    
#     clauses = []
    
#     for instance in n:
        
        
    
    
    
def can_turn_off_lights(input_file_path, output_file_path):
    '''
        This function will contain your code.  It wil read from the file <input_file_path>,
        and will write its output to the file <output_file_path>.
    '''
    instances = parse_input(input_file_path)
        
    results = []
    formula = None
    
    # for line in lines:
    #     line = line.strip()
    #     if line.startswith("***"):
    #         if formula != None:
    #             result = two_sat_solver(formula)
    #             results.append(result)
            
    #         formula = two_cnf()
    #     else:
    #         if formula is not None:
    #             clause = line.split(',')
    #             clause = [literal.strip() for literal in clause]
    #             formula.add_clause(clause)
    # if formula is not None:
    #     result = two_sat_solver(formula)
    #     results.append(result)
    
    m = 0
    n = 0
    lights = {}
    connections = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith("***"):
            # nums = line.split(',')
            # m = nums[0]
            # n = nums[1]
            continue
        else:
            
            print("help")
            
    #         if formula is not None:
    #             clause = line.split(',')
    #             clause = [literal.strip() for literal in clause]
    #             formula.add_clause(clause)
    # if formula is not None:
    #     result = two_sat_solver(formula)
    #     results.append(result)


    # Write results to the output file
    with open(output_file_path, 'w') as outfile:
        for result in results:
            outfile.write(str(result))
            
    def input_converter(n, m, light_arr, connections_arr):
        print ("nothing")

    print(str(m))
neg = '~'


# directed graph class
#  adapted from:
#  src: https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/
class dir_graph:
    def __init__(self):
        # create an empty directed graph, represented by a dictionary
        #  The dictionary consists of keys and corresponding lists
        #  Key = node u , List = nodes, v, such that (u,v) is an edge
        self.graph = defaultdict(set)
        self.nodes = set()

    # Function that adds an edge (u,v) to the graph
    #  It finds the dictionary entry for node u and appends node v to its list
    # performance: O(1)
    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.nodes.add(u)
        self.nodes.add(v)

    # Function that outputs the edges of all nodes in the graph
    #  prints all (u,v) in the set of edges of the graoh
    # performance: O(m+n) m = #edges , n = #nodes
    def print(self):
        edges = []
        # for each node in graph
        for node in self.graph:
            # for each neighbour node of a single node
            for neighbour in self.graph[node]:
                # if edge exists then append
                edges.append((node, neighbour))
        return edges


# 2-CNF class
#  Class storing a boolean formula in Conjunctive Normal Form of literals
#  where the size of clauses is at most 2
#  -NOTATION-
#    The CNF is represented as a list of lists
#    e.g [[x, y], [k, z]] == (x or y) and (k or z)
#    i.e Conjunction of inner lists , where the inner lists are disjunctions
#    of literals
#    Negation is represented with ~ .  ~x == negation of literal x
# class two_cnf:
class two_cnf:
    def __init__(self):
        self.con = []

    # adds a clause to the CNF
    # performance O(1)
    def add_clause(self, clause):
        if len(clause) <= 2:
            self.con.append(clause)
        else:
            print("error: clause contains > 2 literals")

    # returns a set of all the variables in the CNF formula
    def get_variables(self):
        vars = set()
        for clause in self.con:
            for literal in clause:
                vars.add(literal)
        return vars

    def print(self):
        print(self.con)


# helper function that applies the double negation rule to a formula
#   the function removes all occurrences ~~ from the formula
def double_neg(formula):
    return formula.replace((neg+neg), '')


# Function that performs Depth First Search on a directed graph
# O(|V|+|E|)
def DFS(dir_graph, visited, stack, scc):
    for node in dir_graph.nodes:
        if node not in visited:
            explore(dir_graph, visited, node, stack, scc)


# DFS helper function that 'explores' as far as possible from a node
def explore(dir_graph, visited, node, stack, scc):
    if node not in visited:
        visited.append(node)
        for neighbour in dir_graph.graph[node]:
            explore(dir_graph, visited, neighbour, stack, scc)
        stack.append(node)
        scc.append(node)
    return visited


# Function that generates the transpose of a given directed graph
# Performance O(|V|+|E|)
def transpose_graph(d_graph):
    t_graph = dir_graph()
    # for each node in graph
    for node in d_graph.graph:
        # for each neighbour node of a single node
        for neighbour in d_graph.graph[node]:
            t_graph.addEdge(neighbour, node)
    return t_graph


# Function that finds all the strongly connected components in a given graph
# Implementation of Kosaraju’s algorithm
# Performance O(|V|+|E|) for a directed graph G=(V,E)
# IN : directed graph, G
# OUT: list of lists containing the strongly connected components of G
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


# Function that finds a contradiction in a list of strong connected components
# if [a , b , ~a,  c, a] is a connected component then the function returns T
# since a -> ~a -> a exists
# sccs = Strongly Connected Components
#   It is a list of lists representing the connected components
def find_contradiction(sccs):
    for component in sccs:
        for literal in component:
            for other_literal in component[component.index(literal):]:
                if other_literal == double_neg(neg + literal):
                    return True
    return False


# Function that determines if a given 2-CNF is Satisfiable or not
def two_sat_solver(two_cnf_formula):
    print("Checking if the following 2-CNF is Satisfiable in linear time ")
    two_cnf_formula.print()
    # setup the edges of the graph
    # G = (V,E) , V = L U ~L where L = set of variables in 2-CNF
    # E =
    # {(~u,v),(~v,u) | for all clauses [u,v] } U {(~u,u) | for all clauses [u]}
    graph = dir_graph()
    for clause in two_cnf_formula.con:
        if len(clause) == 2:
            u = clause[0]
            v = clause[1]
            graph.addEdge(double_neg(neg+u), v)
            graph.addEdge(double_neg(neg+v), u)
        else:
            graph.addEdge(double_neg(neg+clause[0]), clause[0])
    if not find_contradiction(strongly_connected_components(graph)):
        print("2-CNF Satisfiable")
    else:
        print("2-CNF not Satisfiable")


# [a, b, a, c, ~b, d]
# ======= 2-CNF setup =======
# formula = two_cnf()
# formula.add_clause(['a', 'b'])
# formula.add_clause(['~a', 'b'])
# formula.add_clause(['a', '~b'])
# formula.add_clause(['~a', '~b'])
two_sat_solver(formula)


'''
    To test your function, you can uncomment the following command with the the input/output
    files paths that you want to read from/write to.
'''
# can_turn_off_lights('inputs/input2.txt', 'output.txt')
