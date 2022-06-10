import graphviz as gz

# Grammar input  RL
Vn = ['S', 'A', 'B', 'C']
Vt = ['a', 'b']
P = ["S=bA", "A=aS", "S=aB", "B=aC", "C=aQ", "C=bS"]

# Make the link between the states
link_fa = {}
count = 0

for element in Vn:
    link_fa[element] = "q{}".format(count)
    count += 1

link_fa['Q'] = "q{}".format(count)

finite_automaton = {}

for transition in P:
    if link_fa[transition[0]] not in finite_automaton.keys():
        finite_automaton[link_fa[transition[0]]] = []
    finite_automaton[link_fa[transition[0]]].append(tuple([transition[-2], link_fa[transition[-1]]]))

print(finite_automaton)

def is_accepted (string, fa, idx=0, node='q0'):
    for weight, adj_node in fa[node]:
        if string[idx] == weight:
            if adj_node == link_fa['Q'] and idx == (len(string) - 1):
                print("YES")
                return 0
            else:
                return is_accepted (string, fa, idx + 1, node=adj_node)
    print("NO")

is_accepted ("aaa", finite_automaton)




# Initialize the Graph.
graph = gz.Digraph()
graph.attr(rankdir='LR', size='8,5')

# Compute all nodes.
for element in finite_automaton:
    for weight, adj_node in finite_automaton[element]:
        graph.attr('node', shape='circle')
        graph.node(element)

        # Check for the empty node.
        if adj_node == link_fa['Q']:
            graph.attr('node', shape='doublecircle')
            graph.node(adj_node)
        else:
            graph.attr('node', shape='circle')
            graph.node(adj_node)

        # Add the labels.
        graph.edge(element, adj_node, label=weight)

# Add the start arrow.
graph.attr('node', shape='none')
graph.node('')
graph.edge('', 'q0')
graph.view()