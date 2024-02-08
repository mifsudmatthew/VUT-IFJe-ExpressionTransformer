# Developed by Matthew Mifsud

from Scanner import *

# Creating an array acting as a stack which stores each token during the simulation of parse tree construction
expressionStack = []

# Creating a dictionary to define the precedence of each operator, with 1 being the lowest priority
operatorPrecedence = {'-': 1, '+': 1, '*': 2, '/': 2, '%': 2, '^': 3 }

# Creating a function acting as a Semantic action which appends each operator to the stack
# Operators are given ID: 1
def semanticOp(input):
    if(input == ADD):
        expressionStack.append((1,'+'))
    elif(input == SUB):
        expressionStack.append((1,'-'))
    elif(input == MUL):
        expressionStack.append((1,'*'))
    elif(input == DIV):
        expressionStack.append((1,'/'))
    elif(input == POW):
        expressionStack.append((1,'^'))
    elif(input == MOD):
        expressionStack.append((1,'%'))

# Creating a function acting as a Semantic action which appends each number to the stack        
def semanticNum(input):
    expressionStack.append((0,input))

# Creating a function which builds the expression (converts the stack to an expression)   
def expressionBuilder(parseStatus):
    
    # Checking whether parsing was a success
    if(parseStatus == False):
        exit("Syntax Error Occurred")
    
    # Making sure user has inputted some tokens
    if(len(expressionStack)==0):
        exit("No tokens found (Empty input file)")

    temp = [] # Creating an array to temporarily store the expression
    currentOperator = "" # Creating a variable to store the inner most operator in the stack
    nextOperator = "" # Creating a variable to store the operator which comes after 'currentOperator'
    operatorList = [] # Creating an array to store the list of operators in the entire expression in their respective order
    rightAssociative = False # Creating a boolean variable to keep track if sub expression is right associative
    elimBrackets = False # Creating a boolean variable to keep track if sub expression doesn't need brackets in a special case
    addBrackets = False # Creating a boolean variable to keep track if sub expression needs brackets in a special case
    
    # Obtaining all operators from the stack and storing them in 'operatorList'
    for operator in expressionStack:
        
        if(operator[1] in {'-', '+', '*', '/', '%', '^' }):
            
            operatorList.append(operator[1])

    while(len(expressionStack)!=0): # Looping until stack is empty
        
        if(expressionStack[-1][0] == 0): # If token is a number
            
            number = expressionStack.pop() # Number is popped from stack
            
            number = number[1] # The actual number is obtained (removing ID and tuple)
            
            temp.append(str(number)) # Number is appended to a temporary list
        
        if(expressionStack[-1][0] == 1): # If token is an operator
            
            temp.append(expressionStack.pop()) # Operator is popped from stack
            
            operator = temp.pop() # Operator is popped from stack

            operator = operator[1] # The actual operator is obtained (removing ID and tuple)
            
            # Checking if the ^ operator is in parameter 1
            if(len(expressionStack)>=1 and expressionStack[-1][1]=='^' and operator=='^'):
                
                rightAssociative = True # If so, it requires brackets
                
            # Checking if inner operator in stack has same precedence as the next operator 
            if(len(expressionStack)>=1 and (expressionStack[-1][1] in {'-', '+', '*', '/', '%'}) and (operator in {'-', '+', '*', '/', '%'}) and (operatorPrecedence[expressionStack[-1][1]]==operatorPrecedence[operator])):
                
                elimBrackets = True # If so, it does not require brackets
            
            # Checking if current token is a second parameter, and the first parameter has lower or same priority
            if(len(expressionStack)>=3 and expressionStack[-1][0]==0 and expressionStack[-2][0]==0 and expressionStack[-3][0]==1 and operatorPrecedence[operator] >= operatorPrecedence[expressionStack[-3][1]]):
                
                addBrackets = True # If so, it requires brackets
                
            # Checking if current token is + or - and is a second parameter, and the first parameter has lower or same priority
            elif(len(expressionStack)==2 and expressionStack[-1][0]==0 and expressionStack[-2][0]==1 and operator in {'+','-'}  and operatorPrecedence[operator] >= operatorPrecedence[expressionStack[-2][1]]):
                
                addBrackets = True # If so, it requires brackets
            
            parameter1 = temp.pop() # Popping parameter 1 from stack
            parameter2 = temp.pop() # Popping parameter 2 from stack

            currentOperator = operatorList.pop() # Popping the current operator from stack
            
            if(len(operatorList)!=0): # If list of operators is not empty
                
                nextOperator = operatorList[-1] # Obtaining the next operator after the current one
                
            if(len(operatorList)==0): # If list of operators is empty
                
                # Expression is appended to the temporary list and brackets are not required
                temp.append(parameter1 + " " + operator + " " + parameter2)
            
            # If the current and next operator are both '^' and right associativity is not required
            elif(currentOperator==nextOperator and currentOperator=='^' and rightAssociative==False):
                
                # Expression is appended to the temporary list and brackets are not required
                temp.append(parameter1 + " " + operator + " " + parameter2)            
             
            # If the current and next operator are both '^' and right associativity is required    
            elif(currentOperator==nextOperator and currentOperator=='^' and rightAssociative==True):
                
                # Expression is appended to the temporary list and brackets are required
                temp.append("(" + parameter1 + " " + operator + " " + parameter2 + ")") 
                
                rightAssociative = False  # Resetting 'rightAssociative' variable

            # If the current operator has a greater precedence than the next operator and brackets are not required
            elif(operatorPrecedence[currentOperator]>=operatorPrecedence[nextOperator] and addBrackets==False):
                
                # Expression is appended to the temporary list and brackets are not required
                temp.append(parameter1 + " " + operator + " " + parameter2)
            
            # If the current operator has a greater precedence than the next operator and brackets are required
            elif(operatorPrecedence[currentOperator]>=operatorPrecedence[nextOperator] and addBrackets==True):
                
                # Expression is appended to the temporary list and brackets are required
                temp.append("(" + parameter1 + " " + operator + " " + parameter2 + ")")
                
                addBrackets = False # Resetting 'addBrackets' variable
            
            # If the current operator is the same as the next operator but not a '^' (since it is right associative)    
            elif(currentOperator==nextOperator and currentOperator!='^'):
                
                # Expression is appended to the temporary list and brackets are not required
                temp.append(parameter1 + " " + operator + " " + parameter2)
            
            # If the current operator has the same precedence as the next operator and brackets should not be eliminated  
            elif(operatorPrecedence[currentOperator]==operatorPrecedence[nextOperator] and elimBrackets==False):               

                # Expression is appended to the temporary list and brackets are required
                temp.append("(" + parameter1 + " " + operator + " " + parameter2 + ")")
            
            # If the current operator has the same precedence as the next operator and brackets should be eliminated    
            elif(operatorPrecedence[currentOperator]==operatorPrecedence[nextOperator] and elimBrackets==True):               

                # Expression is appended to the temporary list and brackets are not required
                temp.append(parameter1 + " " + operator + " " + parameter2)
                
                elimBrackets = False # Resetting 'elimBrackets' variable
                
            else: # In any other case
                
                # Expression is appended to the temporary list and brackets are added
                temp.append("(" + parameter1 + " " + operator + " " + parameter2 + ")")

    temp = temp[0] # Obtaining the completed expression from the array
    
    return temp # Expression is returned     


    


