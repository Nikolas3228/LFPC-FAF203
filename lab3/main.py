
import lexer

def main():
    #Read the source code 
    content = "" 

    with open ('test.lang', 'r') as file : 
        content = file.read()

    #Lexer
    #We call the lexel class and intialize it with source code
    lex = lexer.Lexer(content)
    #Call the tokenize method
    tokens = lex.tokenize()
main()
