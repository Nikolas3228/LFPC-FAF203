NFA = {}
inputs = ['a', 'b']
states = ['q0', 'q1', 'q2', 'q3']
transitions = [
               ['q0', 'a', 'q0'], 
               ['q0', 'a', 'q1'], 
               ['q1', 'b', 'q2'], 
               ['q2', 'a', 'q2'], 
               ['q3', 'a', 'q3'],
               ['q2', 'b', 'q3']
               ]


for transition in transitions:
    if transition[0] not in NFA.keys():
        NFA[transition[0]] = []
    NFA[transition[0]].append([transition[1], transition[2]])


print ("Input", NFA)

def check_states(str, set):
    for c in str:
        if ''.join(sorted(c)) == ''.join(sorted(set)):
            return True
    return False


def NFAtoDFA():
    for state in states:
        if state in NFA.keys():
            for input in inputs:
                new_state = ''
                adj_states = []
                has_same_input = 0
                for transition in NFA[state]:
                    if input == transition[0]:
                        has_same_input += 1
                        new_state += transition[1]
                        adj_states.append(transition[1])
                if has_same_input > 1:
                    if check_states(NFA.keys(), new_state):
                        return
                    NFA[new_state] = []
                    for adj_state in adj_states:
                        for trans in NFA[adj_state]:
                            if trans not in NFA[new_state]: 
                                NFA[new_state].append(trans)
                    states.append(new_state)

NFAtoDFA()

print("DFA", NFA)