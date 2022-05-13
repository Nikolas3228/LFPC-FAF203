import copy

#
# check if a given grammer
# exist left-recusion or left-refactor
#
def ll1_check(p_hash):
    invalid_p = []
    # iterate grammer, key is symbol
    # value is production array,
    # check symbol by symbol
    #
    for sym, p in p_hash.items():
        prefix = []
        for pro in p:
            # check left-recusion
            if pro[0]==sym:
                invalid_p.append([sym, pro, "left-recusion"])
            # check left refactoring
            if pro[0] in prefix:
                invalid_p.append([sym, pro, "left-refactor"])
            # store the found prefix for next left-refactor check
            prefix.append(pro[0])
    return invalid_p

#
# check if a given grammer's
# first_hash and follow_hash has some conflict
#
def ll1_first_follow_check(first_hash, follow_hash):
    invalid_p = []
    #
    # first-follow conflict check
    # iterate first_hash, key is symbol
    # value is the symbol's first item array
    #
    for k,v in first_hash.items():
        if k in follow_hash:
            #
            # find out if any item be contained both in the symbol's follow array
            # and first array
            #
            if len(set(v) & set(follow_hash[k])) > 0:
                invalid_p.append([k, v, follow_hash[k], "first-follow-conflict"])
    return invalid_p

# generate first array
def gen_first(sym, p_hash, term_syms, unterm_syms, empty_sym):
    # only care about first item
    sym = sym[0] 
    if sym in term_syms:
        return [sym]
    
    first_set = []
    for s in p_hash[sym]:
        #check if 1symbol is empty
        if s==empty_sym:
            if len(sym) > 1:
                first_set += gen_first(sym[1:], p_hash, term_syms, unterm_syms, empty_sym)
            else:
                first_set += [empty_sym]
            #print(first_set)
        else:
            #all other cases
            sub_first_set = gen_first(s, p_hash, term_syms, unterm_syms, empty_sym)
            #print(sub_first_set)
            first_set += sub_first_set
    
    return first_set

# generate follow array
def gen_follow(sym, p_hash, term_syms, unterm_syms, empty_sym, result):
    if len(sym) != 1:
        return {}

    for key in p_hash.keys():
        for value in p_hash[key]:
            if sym in value:
                index = value.index(sym)
                #check for case if after the non-terminal is empty..
                if index == (len(value) - 1):
                    if key != sym:
                        if key in result:
                            temp = result[key]
                        else:
                            result = gen_follow(key, p_hash, term_syms, unterm_syms, empty_sym, result)
                            temp = result[key]
                        result[sym] += temp
                else:
                    #check the case after  non terminal is a terminal
                    first_of_next = gen_first(value[index + 1:], p_hash, term_syms, unterm_syms, empty_sym)
                    #this terminal contains empty
                    if empty_sym in first_of_next:
                        if key != sym:
                            if key in result:
                                temp = result[key]
                            else:
                                result = gen_follow(key, p_hash, term_syms, unterm_syms, empty_sym, result)
                                temp = result[key]
                            result[sym] += temp
                            result[sym] += first_of_next + [empty_sym]
                    #this terminal doesn't contains empty
                    else:
                        result[sym] += first_of_next
                result[sym] = list(set(result[sym]))
    return result

# generate ll(1) table
def gen_ll_1_table(p_hash, first_hash, follow_hash, empty_sym):
    table = {}
    for key in p_hash.keys():
        for value in p_hash[key]:
            #add elements for first_hash
            if value != empty_sym:
                for element in first_hash[value[0]]:
                    table[key, element] = value
            #add elements for follow_hash
            else:
                for element in follow_hash[key]:
                    table[key, element] = value
    #update table with new pairs
    new_table = {}
    for pair in table:
        new_table[pair[1]] = {}

    for pair in table:
        new_table[pair[1]][pair[0]] = table[pair]

    return table

# parse a given language use ll(1) method
def parse(ll1_table, start_symbol, empty_sym, input_program):
    end_sym = "$"
    user_input = input_program + end_sym
    stack = [end_sym, start_symbol]

    input_len = len(user_input)
    index = 0
    parse_hist = []
    #Check if stack still contain symbol
    while len(stack) > 0:
        top = stack[-1]
        act_p = None
        act_stub = [copy.copy(stack), copy.copy(user_input[index:]), None]
        current_input = user_input[index]
        #check if stack==input ->remove it
        if top == current_input:
            stack.pop()
            index = index + 1
        else:#search in table to decide which production to expand
            key = top, current_input
            if key not in ll1_table: # if not find any production, not accept this language
                print(str(key)+" not in table "+str(ll1_table))
                return False,parse_hist
            #change the key value with value from ll1 table
            value = ll1_table[key]
            # find one, the update current expand action
            act_stub[2] = str(key[0])+" -> "+str(value)
            if value != empty_sym:
                 # expand this production on stack
                value = value[::-1]
                value = list(value)
                stack.pop()
                for element in value:
                    stack.append(element)
            else:
                stack.pop()
            parse_hist.append(act_stub)
    # if all input eliminated then accept this program
    return True,parse_hist

#
# pretty dump the parse result
#
def dump_parse_hist(parse_hist, language, result):
    if parse_hist is None:
        print("Parse language '"+language+"', not accept.")
    else:
        if result:
            print("Parse language '"+language+"', accept:")
        else:
            print("Parse language '"+language+"', not accept:")
        columns = ["Stack", "Input", "Production"]
        rows = []
        # decide the max width for each column, this is used to pretty-print the table
        # not depends on each row's actually width
        columns_width = [len(x) for x in columns]
        for ind in range(0, len(parse_hist)):
            rows.append([str(parse_hist[ind][0]), str(parse_hist[ind][1]), str(parse_hist[ind][2])])
             # update max column width for each row
            columns_width = [max(columns_width[tmp_ind], len(rows[-1][tmp_ind])) for tmp_ind in range(0, len(columns_width))]
        titles = []
        # according to titles' length and max width, decide the padding items
        # different title has different padding length
        for ind in range(0, len(columns)):
            padding = " "*(columns_width[ind]-len(columns[ind]))
            titles.append(columns[ind] + padding)
        print(' '.join(titles))
        
        # same as padding title, the padding for each row has the same logic
        for row in rows:
            row_str = []
            for ind in range(0, len(columns)):
                padding = " "*(columns_width[ind]-len(row[ind]))
                row_str.append(row[ind] + padding)
            print(' '.join(row_str))

def main():
    # 1. define raw language
    gramar_raw = {
        'S': ['A'],
        'A': ['B', 'BeA'],
        'B': ['abD'],
        'D': ['Cd'],
        'C': ['c', 'Cc'],
    }
    
    # 2. raw language's ll1 language (mannually)
    gramar = {
        'S': ['A'],
        'A': ['BF'],
        'F': ['X', 'eA'],
        'B': ['abD'],
        'C': ['cE'],
        'E': ['cE', 'X'],
        'D': ['Cd']
    }
    
    term_syms = ['a', 'b', 'c', 'd', 'e']
    unterm_syms = ['S', 'A', 'B', 'C', 'D', 'E', 'F']
    empty_sym = 'X'
    start_sym = 'S'
    language = "abcdeabcccd"

    # 
    # 3. check if ll1 gramar is valid or not
    # if is invalid, invalid result will be return and print
    #
    invalid_result = ll1_check(gramar)
    if len(invalid_result) > 0:
        print("Not LL(1), invalid gramar: "+str(invalid_result))
        return

    #
    # 4. get symbol's FIRST array, construct a first-hash
    # which key is symbol, value is the symbol's FIRST array
    #
    first_hash = {}
    #Loop for check until find term symbol
    for l_sym in gramar.keys():
        first_hash[l_sym] = list(set(gen_first(l_sym, gramar, term_syms, unterm_syms, empty_sym)))
    #Loop to add term symbol
    for l_sym in term_syms:
        first_hash[l_sym] = list(set(gen_first(l_sym, gramar, term_syms, unterm_syms, empty_sym)))
    print("First hash: "+str(first_hash))

    #
    # 5. get symbol's FOLLOW array, construct a follow-hash
    # which key is symbol, value is the symbol's FOLLOW array
    #
    follow_hash = {}
    follow_hash[start_sym] = ['$']
    for l_sym in gramar.keys():
        follow_hash[l_sym] = []
    for l_sym in gramar.keys():
        follow_hash = gen_follow(l_sym, gramar, term_syms, unterm_syms, empty_sym, follow_hash)
    for l_sym in follow_hash.keys():
        if not '$' in follow_hash[l_sym]:
            follow_hash[l_sym].append('$')
    print("Follow hash: "+str(follow_hash))

    #
    # 6. check if first-hash and follow-hash
    # has some conflict,
    # if conflict exist, invalid result will be return
    # and invalid result will be print
    #
    invalid_result = ll1_first_follow_check(first_hash, follow_hash)
    if len(invalid_result) > 0:
        print("First_follow conflict, invalid ll1 gramar: "+str(invalid_result))
        return

    #
    # 7. generate ll1 table, for ll(1) parser
    #
    ll_1_table = gen_ll_1_table(gramar, first_hash, follow_hash, empty_sym)
    print(ll_1_table)

    #
    # 8. parse a given checked language
    # the return is:
    #      result -> is true, then this language is accept, else not accept
    #      parse_hist -> parse trace, store the parse process
    #
    result, parse_hist = parse(ll_1_table, start_sym, empty_sym, language)

    #
    # 9. print the parse trace to user
    #
    dump_parse_hist(parse_hist, language, result)
    
if __name__ == "__main__":
    main()
