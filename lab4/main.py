from collections import defaultdict
from itertools import combinations

Vn = ['S','A','B','C','D']
Vt = ['a','b']
  
grRules = ['S->aB','S->bA','S->B','A->b','A->aD','A->AS','B->bAB','A->$','B->a','B->bS','C->AB','D->BB']

def parseGrammar():

  grammar = {}
  
  for tranz in grRules:
    rules = tranz.split("->")
    rule = list(rules[1])
    if not rules[0] in grammar:
      grammar[rules[0]] = []
    grammar[rules[0]].append(rule)
    
  return defaultdict(lambda: "default",grammar=grammar, Vn=Vn, Vt=Vt)

parsedGrammar = parseGrammar()

def check_eps(grammar):
  eps_rules = []

  for lft_prod in grammar:
    for rght_prod in grammar[lft_prod]:
      if '$' in rght_prod and len(rght_prod) == 1:
        eps_rules.append(lft_prod)
  
  return eps_rules

# Check the frequence of a non-terminal in a production.
def check_frequence(rght_prod, nonTerm, symbol_freq):
  freq = 0;
  for index in range(len(rght_prod)):
    if rght_prod[index] == nonTerm:
      freq += 1
      if freq == symbol_freq:
        return index

# Create all possible subsets of a production.
def subsets(rght_prod, remove_tranz, has_eps):
  # Init array for possible combinations
  possible_comb = []
  for x in range(1, has_eps + 1):
    possible_comb += list(combinations(range(1, has_eps + 1), x))
  

  all_comb = []
  for combination in possible_comb:
    # Copy the transition to compute.
    comb = rght_prod.copy()
    for number in combination:
      # Remove the empty state to create a new combination.
      comb.pop(check_frequence(rght_prod, remove_tranz, number) - len(rght_prod) + len(comb))
    # If the combination doesn't exists - add it to the list.
    if comb not in all_comb:
      all_comb.append(comb)

  return all_comb

def remove_epsilon(grammar):
    
  while(len(check_eps(grammar))):
    eps_rules = check_eps(grammar)
    
    for derives_eps in eps_rules:
      for lft_prod in grammar:
        for rght_prod in grammar[lft_prod]:
          # Check if the empty state is in any right production.
          if derives_eps in rght_prod:
            # Count how many empty states are in the production.
            has_eps = rght_prod.count(derives_eps)

            # If all the rules derives to the empty state - make the current state empty.
            if has_eps == len(rght_prod):
              grammar[lft_prod].append(['$'])
              continue

            # Compute the possible combinations.
            possibleCombinations = subsets(rght_prod, derives_eps, has_eps)
            # Update the grammar with the new transitions.
            for comb in possibleCombinations:
              if comb not in grammar[lft_prod]:
                grammar[lft_prod].append(comb)

      # Remove epsilon transitions.
      grammar[derives_eps].remove(['$'])
  return grammar

def remove_unit(grammar, Vn):
  for lft_prod in grammar:
    for rght_prod in grammar[lft_prod]:
      # Check if the states derives in a single Non-Terminal Symbol.
      if len(rght_prod) == 1 and rght_prod[0] in Vn:
        # If true - remove it.
        grammar[lft_prod].remove(rght_prod)
        for rght_rule in grammar[rght_prod[0]]:
          if rght_rule not in grammar[lft_prod]:
            # Update the current state' transition to the adj state transition.
            grammar[lft_prod].append(rght_rule)
  return grammar

def remove_inaccessible(grammar, Vn):
  nonTerms = Vn.copy();
  nonTerms.remove("S")

  for nonTerminal in nonTerms:
    isInaccessible = True

    for lft_prod in grammar:
      for rght_prod in grammar[lft_prod]:
        if nonTerminal in rght_prod and lft_prod != nonTerminal:
            isInaccessible = False
            break
    
    if isInaccessible:
      grammar.pop(nonTerminal)
  return grammar


print('\nStep 1: Eliminate epsilon productions')
eliminate_eps_prod = remove_epsilon(parsedGrammar['grammar'])
print(eliminate_eps_prod)

print('\nStep 2: Eliminate unit productions')
eliminate_unit_prod = remove_unit(eliminate_eps_prod, parsedGrammar['Vn'])
print(eliminate_unit_prod)

print('\nStep 3: Eliminate inaccesible productions')
eliminate_inaccessible_prod = remove_inaccessible(eliminate_unit_prod, parsedGrammar['Vn'])
print(eliminate_inaccessible_prod)
