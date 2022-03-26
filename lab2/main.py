import pandas as pd

grammar = [
    '0 a 0',
    '0 a 1',
    '1 b 2',
    '2 a 2',
    '3 a 3',
    '2 b 3'
]

#for each state we create a dictionary which is keyed by the letters of our alphabet {a,b}
#and the global dictionary is keyed by the states of our NFA

def parseGrammar(grammar):

    nfa = {}
    for grammarRules in grammar:
        rulePart = grammarRules.split(' ')

        if not rulePart[0] in nfa:
            nfa[rulePart[0]] = {}

        if not rulePart[1] in nfa[rulePart[0]]:
            nfa[rulePart[0]][rulePart[1]] = ''

        nfa[rulePart[0]][rulePart[1]] += rulePart[2]

    return nfa


#the algorithm for converting NFA to DFA
#we determine the set of states and values in nfa and add the new states that's length is bigger than 1

def NFAtoDFA(nfa):

    states = []
    values = []
#add stated to new array
    for state in nfa:
        states.append(state)

#check if new states exists
    for state in nfa:
        for value in nfa[state]:

            if len(nfa[state][value]) > 1:
                if not nfa[state][value] in states:
                    states.append(nfa[state][value])
            else:
                if not nfa[state][value][0] in states:
                    states.append(nfa[state][value][0])
#check new transitions
    for state in nfa:
        for value in nfa[state]:
            if not value in values:
                values.append(value)
#create an empty list for new states
    for state in states:
        if not state in nfa:
            newState = list(state)
            for value in values:
                val = []

#for all the states that derive from the new state formated
#we add the transitions to val list
                for st in newState:
                    if value in nfa[st]:
                        val.append(nfa[st][value])
#we add the new state in the global dict keyed by states
                if not state in nfa:
                    nfa[state] = {}
#add the elements of the list to the inner dict which is keyed by alphabet elements
#the values in the inner dict are joined as all the transitions from the formed state are considered
                nfa[state][value] = ''.join(set(''.join(val)))
                states.append(''.join(set(''.join(val))))

    return nfa

print("The initial NFA")
nfa = parseGrammar(grammar)
print(nfa)
NFA = pd.DataFrame(nfa)
NFA = NFA.fillna("X")
print(NFA.transpose())

print("The DFA after conversion")
dfa = NFAtoDFA(nfa)
print(dfa)
DFA = pd.DataFrame(dfa)
DFA = DFA.fillna("X")
print(DFA.transpose())