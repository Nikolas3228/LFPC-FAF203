grammar = [
    'S->A',
    'A->B',
    'A->BeA',
    'B->abD',
    'D->Cd',
    'C->c',
    'C->Cc'
]
term=['e','a','b','d','c']
non_term=['S','A','B','D','C']

def parseGrammar():
    fa = {}
    for rulepart in grammar:
        x = rulepart.split('->')
        if not x[0] in fa:
            fa[x[0]] = []

        symbols = []
        for symbol in x[1]:
            symbols.append(symbol)
        fa[x[0]].append(symbols)

    return fa

dict = parseGrammar()

start_symbol = 'S'

print('First/Last table')


# keys the non-terminals
# values a set for first symbols and a set for last symbols

index = []
first = []
last = []

for symbol in dict:
    index.append(symbol)
    to_find = []
    to_find.append(symbol)
    found = []
    first_symbol = []

    # FIRST SET
    i = 0
    while i < len(to_find):
        if to_find[i] in dict:
            found.append(to_find[i])
            for rule in dict[to_find[i]]:
                if rule[0] not in first_symbol:
                    first_symbol.append(rule[0])
                if rule[0] in non_term and rule[0] not in found:
                    to_find.append(rule[0])
        i += 1

    first.append(first_symbol)
    to_find = []
    to_find.append(symbol)
    found = []
    last_symbol = []

    # LAST SET
    i = 0
    while i < len(to_find):
        if to_find[i] in dict:
            found.append(to_find[i])
            for rule in dict[to_find[i]]:
                if rule[-1] not in last_symbol:
                    last_symbol.append(rule[-1])
                if rule[-1] in non_term and rule[-1] not in found:
                    to_find.append(rule[-1])
        i += 1
    last.append(last_symbol)

# print the FIRST LAST table

print('\t{:<5} {:<25} {:25}'.format('', ' FIRST', 'LAST'))
for i in range(5):
    print('\t{:<5}: {:<15} {:15}'.format(index[i], str(first[i]), str(last[i])))



idx = 0
# create a dictionary with terminals and nonterminals
all_symbols = {}
for symbol in non_term:
    all_symbols[symbol] = idx
    idx += 1

for symbol in term:
    all_symbols[symbol] = idx
    idx += 1

#print(all_symbols)

matrix= [[[] for x in range(idx + 1)] for y in range(idx + 1)]
idx = 1
# Append the nonterminals
for symbol in non_term:
    matrix[0][idx].append(symbol)
    matrix[idx][0].append(symbol)
    idx +=1
# Append the terminals
for symbol in term:
    for ch in symbol:
        matrix[0][idx].append(ch)
        matrix[idx][0].append(ch)
    idx +=1
#print(matrix)

# First Rule | Look for *=*
for key in dict:
    for prod in dict[key]:
        if len(prod) > 1:
            for idx in range(len(prod) - 1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                # Update the matrix with =
                if '=' not in matrix[all_symbols[first_symbol] + 1][all_symbols[second_symbol] + 1]:
                    matrix[all_symbols[first_symbol] + 1][all_symbols[second_symbol] + 1].append('=')


# Second Rule | terminal < FIRST(nonterminal)
for key in dict:
    for prod in dict[key]:
        if len(prod) > 1:
            for idx in range(len(prod) - 1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                if second_symbol in non_term:
                    second_index = index.index(second_symbol)
                    for s in first[second_index]:
                    # Update the matrix with <
                        if '<' not in matrix[all_symbols[first_symbol] + 1][all_symbols[s] + 1]:
                            matrix[all_symbols[first_symbol] + 1][all_symbols[s] + 1].append('<')

# Third Rule | LAST(nonterminal) > terminal
for key in dict:
    for prod in dict[key]:
        if len(prod) > 1:
            for idx in range(len(prod)-1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                if first_symbol in non_term and second_symbol in term:
                    first_index = index.index(first_symbol)
                    for s in last[first_index]:
                         # Update the matrix with >
                        if '>' not in matrix[all_symbols[s] + 1][all_symbols[second_symbol] + 1]:
                            matrix[all_symbols[s] + 1][all_symbols[second_symbol] + 1].append('>')

def matrix_representation(table):
    for row in table:
        for column in row:
            print('{:<7}'.format(str(column)), end='')
        print()


print('\n\n2.Simple Precedence Matrix')
matrix_representation(matrix)
