import copy

#
# check if a given grammar
# exist left-recusion or left-refactor
# 
def ll1_check(p_hash):
    invalid_p = []
    # iterate grammar, key is symbol
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


# generate first array
def gen_first(sym, p_hash, term_syms, unterm_syms, empty_sym):
    first_set = []

    while True:
        sym = sym[0]

        if sym in term_syms:
            first_set += [sym]
            break

        for s in p_hash[sym]:
            if s == empty_sym:
                first_set += [empty_sym]
            else:
                sym = s
                #print("sym", sym)
                # sub_first_set = gen_first(s, p_hash, term_syms, unterm_syms, empty_sym)
                #first_set += first_set

    return first_set
   


# generate follow array
def gen_follow(sym, p_hash, term_syms, unterm_syms, empty_sym, result):

    for key in p_hash.keys():
        for value in p_hash[key]:
            #print("sym", sym)
            #print ("value", value)
            if sym in value:
                index = value.index(sym)
                #check for case if  non-terminal is last..
                #print("**********", index)
                #check if non-terminal is the last symbol in production
                if index == (len(value) - 1):
                    #check for recursion S->S...
                    if key != sym:
                        #print("key", key)
                        #print("sym", sym)
                        #check if key already added
                        if key in result:
                            #print("result", result)
                            temp = result[key]
                        else:
                            result = gen_follow(key, p_hash, term_syms, unterm_syms, empty_sym, result)
                            temp = result[key]
                        result[sym] += temp
                else:
                    #check the case if non-terminal isn't last
                    first_of_next = gen_first(value[index + 1:], p_hash, term_syms, unterm_syms, empty_sym)
                    #print("first_of_next", first_of_next)
                    #contains empty
                    if empty_sym in first_of_next:
                        if key != sym:
                            if key in result:
                                temp = result[key]
                            else:
                                result = gen_follow(key, p_hash, term_syms, unterm_syms, empty_sym, result)
                                temp = result[key]
                            result[sym] += temp
                            result[sym] += first_of_next + [empty_sym]
                    #doesn't contains empty
                    else:
                        result[sym] += first_of_next
                #remove duplicates
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
# parse  tree
#
def parse_tree(parse_hist, language, result):
    print("Stack", "Input", "Production")
    for row in parse_hist:
        print(row)

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
    print("First hash: ")
    for item in first_hash:
        print(item, first_hash[item])

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
    print("Follow hash: ")
    for item in follow_hash:
        print(item, follow_hash[item])

 
    #
    # 6. generate ll1 table, for ll(1) parser
    #
    ll_1_table = gen_ll_1_table(gramar, first_hash, follow_hash, empty_sym)
    print("LL1 Table:")
    for item in ll_1_table.items():
        print(item)


    #
    # 7. parse a given checked language
    # the return is:
    #      result -> is true, then this language is accept, else not accept
    #      parse_hist -> parse trace, store the parse process
    #
    result, parse_hist = parse(ll_1_table, start_sym, empty_sym, language)

    #
    # 8. print the parse tree to user
    #
    parse_tree(parse_hist, language, result)
    
if __name__ == "__main__":
    main()