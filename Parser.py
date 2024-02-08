# Developed by Matthew Mifsud

from Scanner import *
from SemanticCodeGen import *

tokenList = scan() # Obtaining the token list from the scanner

currentToken = 0 # Creating a global variable to keep track of which token is being accessed

def Expression(): # Function representing the starting non-terminal
    
    global currentToken # Indicating that the variable being referred to is the global variable
    
    validity = False # Creating a variable to store the validity of the expression
    
    if(len(tokenList)==0):
        return True
    
    # Checking if the ID of the first token is that of a Function
    if(tokenList[currentToken][0] in KEYWORD):
        
        # Listing all non-terminals that can be derived from the starting non-terminal
        validity = (operator() and
                    openBracket() and
                    parameter() and
                    comma() and
                    parameter() and
                    closeBracket())
            
    return validity # Returning whether expression is valid or not

# Function to simulate that an operator/keyword always appears at the start of an expression
def operator():
    
    global currentToken # Indicating that the variable being referred to is the global variable
    
    semanticOp(tokenList[currentToken][0]) # Semantic Action to store operator in list
    
    currentToken += 1 # Incrementing the global variable to point to next token
    
    return True # No checks are required since it is already done in Expression()

# Function to simulate that an open bracket always appears after an operator/keyword
def openBracket():
    
    global currentToken # Indicating that the variable being referred to is the global variable
    
    validity = False  # Creating a variable to store the validity of the token
    
    # Making sure that the index of the token being accessed does not exceed token list size
    if(currentToken<len(tokenList)):
        
        # Checking if the ID of the token is that of an open bracket
        if(tokenList[currentToken][0] == OPEN_BRACKET):
            
            validity = True  # Token is valid in its position
    
    currentToken += 1 # Incrementing the global variable to point to next token

    return validity # Returning whether the token's position follows the grammar

# Function to simulate that a number always appears after an open bracket or comma
def number():
    
    global currentToken # Indicating that the variable being referred to is the global variable
    
    validity = False # Creating a variable to store the validity of the token
    
    # Making sure that the index of the token being accessed does not exceed token list size
    if(currentToken<len(tokenList)):
        
        # Checking if the ID of the token is that of a number
        if(tokenList[currentToken][0] == NUMBER):
            
            validity = True # Token is valid in its position
    
    semanticNum(tokenList[currentToken][1]) # Semantic Action to store number in list
    
    currentToken += 1 # Incrementing the global variable to point to next token

    return validity # Returning whether the token's position follows the grammar

# Function to simulate that a parameter (nested expression or number) appears after an open bracket or comma
def parameter():
    
    numValidity = False # Creating a variable to store the validity of the token
    
    expValidity = Expression() # Creating a variable to store the validity of the token
    
    if(not expValidity): # If parameter is not an expression but a number
        numValidity = number() # Checking the validity of the token

    return (expValidity or numValidity)  # Returning whether the token's position follows the grammar

# Function to simulate that a comma always appears after the first parameter 
def comma():
    
    global currentToken # Indicating that the variable being referred to is the global variable
    
    validity = False # Creating a variable to store the validity of the token
    
    # Making sure that the index of the token being accessed does not exceed token list size
    if(currentToken<len(tokenList)):
        
        # Checking if the ID of the token is that of a comma
        if(tokenList[currentToken][0] == COMMA):
            
            validity = True # Token is valid in its position
    
    currentToken += 1 # Incrementing the global variable to point to next token

    return validity # Returning whether the token's position follows the grammar

# Function to simulate that a closing bracket always appears after the second parameter 
def closeBracket():
    
    global currentToken # Indicating that the variable being referred to is the global variable
    
    validity = False # Creating a variable to store the validity of the token
    
    # Making sure that the index of the token being accessed does not exceed token list size
    if(currentToken<len(tokenList)):
    
        # Checking if the ID of the token is that of a closing bracket
        if(tokenList[currentToken][0] == CLOSE_BRACKET):
            
            validity = True # Token is valid in its position
    
    currentToken += 1 # Incrementing the global variable to point to next token

    return validity # Returning whether the token's position follows the grammar

# Function to run parser
def parse():
    
    # Making sure there are no extra symbols after expression
    if(Expression() and currentToken==len(tokenList)):    
        return True
    else:
        return False