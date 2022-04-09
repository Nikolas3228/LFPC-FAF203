from collections import defaultdict
from itertools import combinations

Vn = ['S','A','B','C','D']
Vt = ['a','b']
  
productions = ['S->aB','S->bA','S->B','A->b','A->aD','A->AS','B->bAB','A->$','B->a','B->bS','C->AB','D->BB']

def parseGrammar():
  grammar = {}
  
  for transtions in productions:
    rules = transtions.split("->")
    rule = list(rules[1])
    if not rules[0] in grammar:
      grammar[rules[0]] = []
    grammar[rules[0]].append(rule)
    
  return defaultdict(lambda: "default",grammar=grammar, Vn=Vn, Vt=Vt)

parsedGrammar = parseGrammar()

def checkEpsilon(grammar):
  epsilon_rules = []

  for state in grammar:
    for transitions in grammar[state]:
      if '$' in transitions and len(transitions) == 1:
        epsilon_rules.append(state)
  return epsilon_rules

# Check the frequence of a non-terminal in a production.
def checkFrequency(transitions, non_term, symbol_freq):
  freq = 0;
  for index in range(len(transitions)):
    if transitions[index] == non_term:
      freq += 1
      if freq == symbol_freq:
        return index

# Create all possible subsets of a production.
def subsets(transitions, remove_transition, has_epsilon):
  # Init array for possible combinations
  possible_combinations = []
  for x in range(1, has_epsilon + 1):
    possible_combinations += list(combinations(range(1, has_epsilon + 1), x))
  
  new_transitions = []
  for combination in possible_combinations:
    # Copy the transition to compute.
    comb = transitions.copy()
    for number in combination:
      # Remove the empty state to create a new combination.
      comb.pop(checkFrequency(transitions, remove_transition, number) - len(transitions) + len(comb))
    # If the combination doesn't exists - add it to the list.
    if comb not in new_transitions:
      new_transitions.append(comb)

  return new_transitions

def removeEpsilon(grammar):
    
  while(len(checkEpsilon(grammar))):
    epsilon_rules = checkEpsilon(grammar)
    
    for derives_eps in epsilon_rules:
      for state in grammar:
        for transitions in grammar[state]:
          # Check if the empty state is in any right production.
          if derives_eps in transitions:
            # Count how many empty states are in the production.
            has_epsilon = transitions.count(derives_eps)

            # If all the rules derives to the empty state - make the current state empty.
            if has_epsilon == len(transitions):
              grammar[state].append(['$'])
              continue

            # Compute the possible combinations.
            possibleCombinations = subsets(transitions, derives_eps, has_epsilon)
            # Update the grammar with the new transitions.
            for comb in possibleCombinations:
              if comb not in grammar[state]:
                grammar[state].append(comb)

      # Remove epsilon transitions.
      grammar[derives_eps].remove(['$'])
  return grammar

def removeUnit(grammar, Vn):
  for state in grammar:
    for transitions in grammar[state]:
      # Check if the states derives in a single Non-Terminal Symbol.
      if len(transitions) == 1 and transitions[0] in Vn:
        # If true - remove it.
        grammar[state].remove(transitions)
        for transition_rules in grammar[transitions[0]]:
          if transition_rules not in grammar[state]:
            # Update the current state' transition to the adj state transition.
            grammar[state].append(transition_rules)
  return grammar

def removeInaccessible(grammar, Vn):
  non_terminals = Vn.copy();
  non_terminals.remove("S")

  for non_terminal in non_terminals:
    inaccessible = True

    for state in grammar:
      for transitions in grammar[state]:
        if non_terminal in transitions and state != non_terminal:
            inaccessible = False
            break
    
    if inaccessible:
      grammar.pop(non_terminal)
  return grammar



print('\nInput', parsedGrammar['grammar'])

print('\nStep 1: Eliminate epsilon productions')
eliminate_eps_prod = removeEpsilon(parsedGrammar['grammar'])
print(eliminate_eps_prod)

print('\nStep 2: Eliminate unit productions')
eliminate_unit_prod = removeUnit(eliminate_eps_prod, parsedGrammar['Vn'])
print(eliminate_unit_prod)

print('\nStep 3: Eliminate inaccesible productions')
eliminate_inaccessible_prod = removeInaccessible(eliminate_unit_prod, parsedGrammar['Vn'])
print(eliminate_inaccessible_prod)
