import re

KEYWORD = ["if", "else", "while", "for", "print", "scan", "return", "switch", "case", "break", "fun", "goto","default"]
SEPARATOR = ['(', ')', '{', '}', '[', ']',',','=']
OPERATOR = ['-', '+', '*', '/', '%']
DATA_TYPE = ['int', 'float','string', 'bool','void']
BOOL_VAL = ['True','False']






class Lexer(object):
    def __init__(self, source_code):
        self.source_code=source_code
    
    def tokenize(self):
        tokens = []

        #1. Word list
        source_code = self.source_code.split()

        #   Index of word list
        source_index = 0

        #Loop through source code for generating tokens
        while source_index < len(source_code):
            word_list  = source_code[source_index]
            if (source_code[source_index]) == ' ':
                self.check
                source_index +=1

            #Token for "KEYWORDS"
            if word_list in KEYWORD : 
                tokens.append(["KEYWORD", word_list])      

            #Token for "SEPARATORS"
            elif word_list in SEPARATOR :
                tokens.append(["SEPARATORS", word_list])

            #Token for "OPERATORS"
            elif word_list in OPERATOR: 
                tokens.append(["OPERATORS", word_list])

            #Token for "DATA_TYPE"
            elif word_list in DATA_TYPE:
                tokens.append(["DATA_TYPE", word_list])

            #Token for "COMMENT"
            elif word_list in "#" :
                tokens.append(["COMMENT", word_list])

            #Token for "BOOL_VAL"
            elif word_list in BOOL_VAL:
                tokens.append(["BOOL_VAL", word_list])
            
            #Token for any unspecified word
            elif re.match('[a-z]', word_list) or re.match('[A-Z]', word_list):
                if word_list[-1] == ";" :
                    tokens.append(["IDENTIFIER", word_list[0:len(word_list)-1]])
                else: 
                    tokens.append(['IDENTIFIER', word_list])


            elif re.match('[0-9]', word_list):
                if word_list[-1] == ";" :
                    tokens.append(["INTEGER", word_list[0:len(word_list)-1]])
                else: 
                    tokens.append(["INTEGER", word_list])

            #don't recheck tokens
            source_index +=1
        print(tokens)
        return tokens