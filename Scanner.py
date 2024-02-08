# Developed by Matthew Mifsud

# SYMBOL TABLE
ADD = 0
SUB = 1
MUL = 2
DIV = 3
POW = 4
MOD = 5  
KEYWORD = {ADD: "add" , SUB: "sub" , MUL: "mul" , DIV: "div", POW: "pow", MOD: "mod"} 
OPEN_BRACKET = 6
CLOSE_BRACKET = 7
COMMA = 8
NUMBER = 9

# Function to return ID/TYPE of a token 
def getKeywordID(STRING):
    
    if(STRING == KEYWORD[ADD]):
        return ADD
    elif(STRING == KEYWORD[SUB]):
        return SUB
    elif(STRING == KEYWORD[MUL]):
        return MUL
    elif(STRING == KEYWORD[DIV]):
        return DIV
    elif(STRING == KEYWORD[POW]):
        return POW
    elif(STRING == KEYWORD[MOD]):
        return MOD

# Main Scanner Functionality
def scan():
    
    # Creating a variable to store the state currently being accessed from the DFA
    state = 'S'
    
    # Creating a tuple containing a set of immutable input symbols (alphabet symbols)
    alphabet = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
    
    # Creating a tuple containing a set of immutable input symbols (numeric symbols)
    numbers = ('0','1','2','3','4','5','6','7','8','9')
    
    # Creating a tuple containing the set of possible signs
    optional_sign = ('+','-')
    
    # Creating a variable to store each token made up of a number of symbols
    string = ""
    
    # Creating a variable to store the list of tokens
    tokenList = []
    
    # Accessing the input source file from which symbols will be read
    source_file = open("input.txt", "r")
    
    # Creating a variable to store each symbol read from the input file
    symbol = ''
    
    # Creating a variable to keep track if End Of File is reached
    EOF = False
    
    # Creating a variable to keep track if a comment was closed
    commentClosed = True
    
    while(not EOF): # Looping until the source file has been read
        
        symbol = source_file.read(1) # Reading a symbol from input file
        
        if not symbol: # Case when end of file is reached
            EOF = True
    
        if(state =='S'): # Entering initial state of the Finite Automata
            
            if(symbol.isspace()): # If empty space is encountered
                continue # Skip iteration to read next symbol
            
            # If symbol read is a letter
            if(symbol in alphabet):
                
                string = symbol # Symbol is saved
                state = "f1" # Move to state 'f1'
                
            # If symbol read is a number or '+' or '-'
            elif(symbol in numbers or symbol in optional_sign):
                
                string = symbol # Symbol is saved
                state = "f2" # Move to state 'f2'
                
            # If symbol read is an open bracket
            elif(symbol == '(' ): 
                
                string = symbol # Symbol is saved
                
                # Symbol is immediately recognised as a token
                tokenList.append((OPEN_BRACKET,string))
                
                state = "S" # Move to state 'S' (start state)
                
            # If symbol read is a closing bracket
            elif(symbol == ')'):
                
                string = symbol # Symbol is saved
                
                # Symbol is immediately recognised as a token
                tokenList.append((CLOSE_BRACKET,string)) 
                
                state = "S" # Move to state 'S' (start state)
            
            # If symbol read is a comma   
            elif(symbol == ','):
                
                string = symbol # Symbol is saved
                
                # Symbol is immediately recognised as a token
                tokenList.append((COMMA,string))
                
                state = "S" # Move to state 'S' (start state)
            
            # If 2 symbols read are a forward slash followed by an asterisk    
            elif(symbol == '/' and source_file.read(1) == '*'):
                
                # Updating variable to indicate the comment needs to be closed
                commentClosed = False
                
                state = "P" # Move to state 'P'
                
            elif(not EOF): # If End Of File has not been reached
                
                # Any other character would make an invalid token
                exit("Invalid token encountered")
            
        elif(state == "f1"): # Entering state 'f1'
            
            # If symbol read is a letter or a number
            if(symbol in alphabet or symbol in numbers):
                
                string += symbol # Symbol is saved or concatenated with the previous symbol
            
            else: # If symbol read is not a letter or a number
                
                # Move back to previous character in source file
                symbol = source_file.seek(source_file.tell() - 1)
                
                # If the string read so far matches a Keyword
                if(string in KEYWORD.values()):
                    
                    # A token is saved to the token list
                    tokenList.append((getKeywordID(string),string))
                else:
                    
                    exit("Invalid tokens encountered")
                          
                state = 'S' # Move to state 'S' (start state)

        elif(state == "f2"): # Entering state 'f2'
            
            if(symbol in numbers): # If symbol read is a number
                
                string += symbol # Symbol is saved or concatenated with the previous symbol
                
            elif(symbol == '.'): # If symbol read is a period
                
                string += symbol # Symbol is saved or concatenated with the previous symbol
                state = "f3" # Move to state 'f3'
        
            elif(symbol == 'e'): # If symbol read is a letter e
                
                string += symbol # Symbol is saved or concatenated with the previous symbol
                state = "f4" # Move to state 'f4'

            # If symbol read is a comma or a bracket or white space or End of File has been reached
            elif(symbol == ',' or symbol == ')' or symbol == '(' or symbol.isspace() or EOF):
                
                # Move back to previous character in source file
                symbol = source_file.seek(source_file.tell() - 1)
                
                tokenList.append((NUMBER,string)) # A token is saved to the token list
                
                state = "S" # Move to state 'S' (start state)  
                   
            else: # If symbol is any other character
                
                exit("Invalid token encountered")
                
        elif(state == "f3"): # Entering state 'f3'
            
            if(symbol in numbers): # If symbol read is a number
                
                string += symbol # Symbol is saved or concatenated with the previous symbol
            
            elif (symbol == 'e'): # If symbol read is a letter e
                
                if(string[-1] == '.'): # If the last symbol in the read string is a period
                    exit("Invalid token encountered")
                else:
                    string += symbol # Symbol is saved or concatenated with the previous symbol
                    state = "f4" # Move to state 'f4'
            
           # If symbol read is a comma or a bracket or white space or End of File has been reached  
            elif(symbol == ',' or symbol == ')' or symbol == '(' or symbol.isspace() or EOF):
            
                # Move back to previous character in source file
                symbol = source_file.seek(source_file.tell() - 1)
                
                tokenList.append((NUMBER,string)) # A token is saved to the token list
                
                state = "S" # Move to state 'S' (start state) 
                   
            else: # If symbol is any other character
                
                exit("Invalid token encountered")
                    
        elif(state == "f4"): # Entering state 'f4'
            
            # If symbol read is a number or '+' or '-'
            if(symbol in numbers or symbol in optional_sign):
                
                # Symbol is saved or concatenated with the previous symbol
                string += symbol
                
                state = "f5" # Move to state 'f5'
            else:
                exit("Invalid token encountered")

        elif(state == "f5"): # Entering state 'f5'
            
            if(symbol in numbers): # If symbol read is a number
                
                string += symbol # Symbol is saved or concatenated with the previous symbol

            # If symbol read is a comma or a bracket or white space or End of File has been reached
            elif(symbol == ',' or symbol == ')' or symbol == '(' or symbol == ' ' or EOF):
                
                 # If the last symbol in the read string is a letter e
                if(string[-1] == 'e'):
                    exit("Invalid token encountered")
                else:
                    
                    # Move back to previous character in source file
                    symbol = source_file.seek(source_file.tell() - 1)
                    
                    tokenList.append((NUMBER,string)) # A token is saved to the token list
                    
                    state = "S" # Move to state 'S' (start state)
                    
            else: # If symbol is any other character
                
                exit("Invalid token encountered")
                
        elif(state == "P"): # Entering state 'P'
            
            # If 2 symbols read are an asterisk followed by a forward slash
            if(symbol == '*' and source_file.read(1) == '/'):
                
                # Updating variable to indicate the comment has been closed
                commentClosed = True
                
                state = "S" # Move to state 'S' (start state)

    if(not commentClosed): # If an unclosed comment was detected
        exit("Unclosed comment")
                                       
    source_file.close() # Closing source file
    
    return tokenList