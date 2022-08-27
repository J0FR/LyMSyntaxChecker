import re

"""
Reserved characters
"""

reservedChars = [',', ';', '{', '}', '(', ')', '=']
reservedNames = ["if", "per", "else", "fi", "while", "do", "od", "PROG", "GORP", "var", "PROC", "CORP", "repeatTimes", "GORP", 
                 "north", "south", "east", "west",
                 "front", "right", "left", "back",
                 "around",
                 # Functions
                 "walk", "jump", "jumpTo", "veer", "look", "drop", "grab", "get", "free", "pop",
                 # Compare Funcitons
                 "isfacing", "isValid", "canWalk", "not"]


"""
Global Variables
"""

localVar = []

varGlobal = []

functionsGlobal = {
        "walk": [1, 2, 3],
        "jump": [1],
        "jumpTo": [2],
        "veer": [1],
        "look": [1],
        "drop": [1],
        "grab": [1],
        "get": [1],
        "free": [1],
        "pop": [1],
        "go": [1],
        "isfacing": [1],
        "isValid": [2],
        "canWalk": [2],
        "not": ["compFunction_type"]
        
    }

compFunctions = {
    "isfacing": [1],
    "isValid": [2],
    "canWalk": [2],
    "not": ["compFunction_type"]
}








# 0 - workingOnVariable | 1 - WorkingVerifyExistingFunction | 2 - workingOnverifyInstructionBlockIfand While |
# 3- working workingOnBlockInstructions | 4 - While loops | 5 - For loops | 6 - Instruction block function creation
# 7 - Creating a function | 8 - Repeat Function
workingOn = [False, False, False, False, False, False, False, False, False]
programError = [False]

        # Working on variables
# Variable 0 = lastTockenVariable? | Variable 1 = lastTockenComma?
workingOnVariableChecks = [False, False]

        # Working on Existing Functions
workingOnExistingFunctionsChecks = [False, False, False, False, True]
usingFunction = None
    
        # Working on Body Conditionals and loops
workingOnBodyConditionalsChecks = [False, False]

        #Working on Block Instructions for ifs and loops
workingOnBlockInstructionsChecks = [False, False, 0]

            #Working while loops
workingOnWhileLoop = [False, False, False, False, False]



workingOnRepeat = [False, False, False, False, False]

            #Working on conditionals
workingOnConditionalsChecks = [False, False, False, False, False, False, False]            

            # Working on instruction block function creation
workingOnInstructionBlockFunctionCreation = [False, False, False, False, False, False]


            # Working on function creation
workingOnFunctionCreation = [False, False, False, False, False, False, False]

        # Not



"""
Main Functions
"""
def parser(tockens: list):

            # Important parser Variables
    tockenNum = 0
    closeParenthesesChecker = False
    
    
    
    
    while tockenNum < len(tockens):
        currentTocken = tockens[tockenNum]
        if programError[0] == False and (currentTocken in reservedNames or currentTocken in reservedChars or (isWorking(workingOn) and validVariableName(currentTocken)) or (isWorking(workingOn) and isNumber(currentTocken))):
            
            if currentTocken == "not" and tockens[tockenNum + 1] == "(":
                print("llegueeee")
                closeParenthesesChecker = True
                tockenNum += 2
                print(tockens[tockenNum])
            if closeParenthesesChecker == True and currentTocken == ")":
                closeParenthesesChecker = False
                tockenNum += 1
            
            if workingOn[0] == True or currentTocken == "var":
                verifyVariableDeclaraction(currentTocken, workingOnVariableChecks, workingOn, programError)
            
            if workingOn[1] == True or currentTocken in functionsGlobal.keys():
                if workingOnExistingFunctionsChecks[4] == True:
                    usingFunction = functionsGlobal[currentTocken]
                    workingOnExistingFunctionsChecks[4] = False
                verifyExistingFunctions(currentTocken, workingOnExistingFunctionsChecks, workingOn, programError, usingFunction)
            
            #if workingOn[7] or currentTocken == "PROC":
            # instructionBlockFunctionCreation(currentTocken, workingOnInstructionBlockFunctionCreation, workingOn, programError)
            FunctionCreation(currentTocken, workingOnFunctionCreation, workingOn, programError)
            
            
            
            # if workingOn[5] or currentTocken == "if":
            #     verifyConditionalsDeclaration(currentTocken, workingOnConditionalsChecks, workingOn, programError)
            
            # if workingOn[4] or currentTocken == "while":
            #     verifyLoopsDeclaration(currentTocken, workingOnWhileLoop, workingOn, programError)
            
            
            
            
            # if (currentTocken == "{" or workingOn[2]):
            #     print(workingOn)
            #     verifyInstructionBlockLoopsAndConditionals(currentTocken, workingOnBodyConditionalsChecks, workingOn, programError)
            # if currentTocken == "(" or workingOn[3]:
            #     verifyConditionBlockLoopsAndConditionals(currentTocken, workingOnBlockInstructionsChecks, workingOn, programError)

           
                    
                    
                    
        else:
            programError[0] = True
            break
        tockenNum += 1
        
    if programError[0] == True:
        print("Master Error")
        print(currentTocken)
        return True
    else:
        return False








































# FUNCTION CREATION
# checks: - var0 = check keyword proc | var1: check that is a valid name for the function
# var2: lst that constains the quantity of variables it accepts | var3: if the next element is the char (
# var4: if the last element was a variable | var5: checks the body instruction
def FunctionCreation(currentTocken: str, checks: list, workingOn: list, programError: bool):
    #ATENTOOOOOOOOOOOOOOOOOOOOOOOOO
    #print(currentTocken)
    if currentTocken == "PROC" and checks[0] == False:
        workingOn[7] = True
        checks[0] = True
        checks[1] = True
    elif checks[1] == True and validVariableName(currentTocken):
        checks[1] = False
        functionsGlobal[currentTocken] = [0]
        checks[2] = functionsGlobal[currentTocken]
        reservedNames.append(currentTocken)
        checks[3] = True
    elif checks[3] == True and currentTocken == "(":
        checks[3] = False
        checks[4] = True
    elif checks[4] == True and (validVariableName(currentTocken)):
        #print(currentTocken)
        #VARIABLES LOCALES
        localVar.append(currentTocken)
        varGlobal.append(currentTocken)
        reservedNames.append(currentTocken)
        num = checks[2][0] + 1
        checks[2] = [num]
        checks[4] = False
    elif checks[4] == False and currentTocken == ",":
        checks[4] = True
    elif checks[4] == False and currentTocken == ")":
        checks[5] = True
    elif checks[5] == True:
        #print(currentTocken)
        instructionBlockFunctionCreation(currentTocken, workingOnInstructionBlockFunctionCreation, workingOn, programError)
        if workingOn[7] == False:
            checks[5] = False
            checks[6] = True
    elif currentTocken == "CORP":
        for i in localVar:
            localVar.remove(i)
            varGlobal.remove(i)
            reservedNames.remove(i)
        workingOn[7] = False
        checks[0]
        checks[1]
        checks[2]
        checks[3]
        checks[4]
        checks[5]
        checks[6]
        checks[7]
    
    else:
        programError[0] = True
        print("ERROR-9")
        print(currentTocken)

# InstructionBlockFunctionCreation
# checks: var0: check { character | var1: checks the current instruction structure | var2: checks that existingFunctionsChecking is done
# var3: woking on conditional declaration | var 4: working on loops declaration
def instructionBlockFunctionCreation(currentTocken: str, checks: list, workingOn: list, programError: bool):
    #print(currentTocken)
    if currentTocken == "{" and checks[0] == False:
        workingOn[6] = True
        checks[0] = True
        checks[1] = True
    
    elif checks[5] == True or (checks[1] == True and currentTocken == "repeatTimes"):
        checks[1] = False
        checks[5] = True
        verifyRepeat(currentTocken, workingOnRepeat, workingOn, programError)
        if workingOn[8] == False:
            checks[5] = False
        
    elif checks[4] == True or (checks[1] == True and currentTocken == "while"):
        checks[1] = False
        checks[4] = True
        verifyLoopsDeclaration(currentTocken, workingOnWhileLoop, workingOn, programError)
        if workingOn[4] == False:
            checks[4] = False
            
            
    elif checks[3] == True or (checks[1] == True and currentTocken == "if"):
        checks[1] = False
        checks[3] = True
        verifyConditionalsDeclaration(currentTocken, workingOnConditionalsChecks, workingOn, programError)
        if workingOn[5] == False:
            checks[3] = False
            
            
    elif checks[1] == True and workingOn[1] == True:
        #print(currentTocken)
        checks[2] = True
    elif workingOn[1] == False and checks[2] == True:
        checks[1] = False
        checks[2] = False
        
        
        
    elif (checks[1] == False and currentTocken == ";"):
        checks[1] = True
    elif (checks[1] == False and currentTocken == "}"):
        workingOn[6] = False
        checks[0] = False
        checks[1] = False
        checks[2] = False
        checks[3] = False
        checks[4] = False
        checks[5] = False
    elif workingOn[6] == False:
        pass
        
        
    else:
        programError[0] = True
        print("ERROR-10")
        print(currentTocken)





# Variable0: verificacion coorchete | Variable1: Finalizo verificacion funcion
def verifyInstructionBlockLoopsAndConditionals(currentTocken: str, checks: list, workingOn: list, programError: bool):
    if checks[0] == False and currentTocken == "{":
        checks[0] = True
        workingOn[2] = True
    elif workingOn[1] == True and checks[1] == False:
        pass
    elif workingOn[1] == False and currentTocken == ";" and checks[1] == True:
        checks[1] = False
    elif workingOn[1] == False and currentTocken == "}" and checks[1] == True:
        checks[0] = False
        checks[1] = False
        workingOn[2] = False
    elif currentTocken == ")":
        checks[1] = True
        
        # pruebaaaaaa
        # checks[0] = False
        # checks[1] = False
        # workingOn[2] = False
        
    else:
        programError[0] = True
        print("ERROR-4")




































# check if conditionals
# checks: var0 - check the open conditional
def verifyConditionalsDeclaration(currentTocken: str, checks: list, workingOn: list, programError: bool):
    if currentTocken == "if" and checks[0] == False:
        workingOn[5] = True
        checks[0] = True
        checks[1] = True
    elif (workingOn[3] or (checks[1] == True and currentTocken == "(")):
        checks[1] = False
        verifyConditionBlockLoopsAndConditionals(currentTocken, workingOnBlockInstructionsChecks, workingOn, programError)
        if workingOn[3] == False:
            checks[2] = True
    elif (workingOn[2] or (checks[2] and currentTocken == "{")):
        checks[2] = False
        verifyInstructionBlockLoopsAndConditionals(currentTocken, workingOnBodyConditionalsChecks, workingOn, programError)
        if workingOn[2] == False:
            checks[3] = True
    # elif (checks[3] and currentTocken == "fi"):
    #     checks[1] = False
    #     checks[2] = False
    #     checks[3] = False
    #     workingOn[5] = False
    elif workingOn[2] or (checks[3] and currentTocken == "else"):
        checks[4] = True
    elif workingOn[2] or (checks[4] and currentTocken == "{"):
        checks[4] = False
        verifyInstructionBlockLoopsAndConditionals(currentTocken, workingOnBodyConditionalsChecks, workingOn, programError)
        print(f"estado {workingOn[2]}")
        if workingOn[2] == False:
            checks[5] = True
    elif currentTocken == "fi":
        print(checks[5])
        checks[0] = False
        checks[1] = False
        checks[2] = False
        checks[3] = False
        checks[4] = False
        checks[5] = False
        workingOn[5] = False
    elif workingOn[5] == False:
        pass
    else:
        programError[0] = True
        print("ERROR-7")
        print(currentTocken)




# check repeat
# checks: var0: check while keyword | var1: conditionals start | var2: verify the do keyword after conditional | var3: check start of instruction block
def verifyRepeat(currentTocken: str, checks: list, workingOn: list, programError: bool):
    #print(currentTocken)
    if currentTocken == "repeatTimes" and checks[0] == False:
        workingOn[8] = True
        checks[0] = True
        checks[1] = True
    elif (checks[1] == True and isNumber(currentTocken)):
        checks[1] = False
        checks[3] = True
    
    elif (workingOn[2] or (checks[3] and currentTocken == "{")):
        checks[3] = False
        verifyInstructionBlockLoopsAndConditionals(currentTocken, workingOnBodyConditionalsChecks, workingOn, programError)
        if workingOn[2] == False:
            checks[4] = True
    elif checks[4] == True and currentTocken == "per":
        checks[0] = False
        checks[1] = False
        checks[2] = False
        checks[3] = False
        checks[4] = False
        workingOn[8] = False
    else:
        programError[0] = True
        print("ERROR-6")




# check while loops
# checks: var0: check while keyword | var1: conditionals start | var2: verify the do keyword after conditional | var3: check start of instruction block
def verifyLoopsDeclaration(currentTocken: str, checks: list, workingOn: list, programError: bool):
    #print(currentTocken)
    if currentTocken == "while" and checks[0] == False:
        workingOn[4] = True
        checks[0] = True
        checks[1] = True
    elif (workingOn[3] or (checks[1] == True and currentTocken == "(")):
        checks[1] = False
        verifyConditionBlockLoopsAndConditionals(currentTocken, workingOnBlockInstructionsChecks, workingOn, programError)
        if workingOn[3] == False:
            checks[2] = True
    elif checks[2] == True and currentTocken == "do":
        checks[2] = False 
        checks[3] = True
    
    elif (workingOn[2] or (checks[3] and currentTocken == "{")):
        checks[3] = False
        verifyInstructionBlockLoopsAndConditionals(currentTocken, workingOnBodyConditionalsChecks, workingOn, programError)
        if workingOn[2] == False:
            checks[4] = True
    elif checks[4] == True and currentTocken == "od":
        checks[0] = False
        checks[1] = False
        checks[2] = False
        checks[3] = False
        checks[4] = False
        workingOn[4] = False
    else:
        programError[0] = True
        print("ERROR-6")
        
    



def verifyVariableDeclaraction(currentTocken: str, checks: list, workingOn: list, programError: bool):
    if workingOn[0] == False and currentTocken == "var":
        workingOn[0] = True
    elif checks[0] == False and validVariableName(currentTocken):
        varGlobal.append(currentTocken)
        reservedNames.append(currentTocken)
        checks[0] = True
    elif checks[0] == True and currentTocken == ",":
        checks[0] = False
    elif checks[0] == True and currentTocken == ";":
        checks[0] = False
        workingOn[0] = False
    else:
        programError[0] = True
        print("ERROR-1")
        workingOn[0] = False
    

        
        
    # Variable 0: openParentesis | Variable 1: checkingVariables | Variable 2: variableCounter | Variable3: lastTockenVariable | variable4: started
def verifyExistingFunctions(currentTocken: str, checks: list, workingOn: list, programError: bool, usingFunction):
    if workingOn[1] == False and (currentTocken in functionsGlobal.keys() or currentTocken in compFunctions.keys()):
        workingOn[1] = True
        checks[0] = True
    elif checks[0] == True and currentTocken == "(":
        checks[0] = False
        checks[1] = True
    elif (checks[1] == True and checks[3] == False): #  and validVariableName(currentTocken)
        checks[2] += 1
        checks[3] = True
    elif checks[1] == True and checks[3] == True and currentTocken == ",":
        checks[3] = False
    elif currentTocken == ")":
        if checks[2] not in usingFunction:
            programError[0] = True
            print("ERROR-2")
            print(currentTocken)
        checks[0] = False
        checks[1] = False
        checks[2] = 0
        checks[3] = False
        checks[4] = True
        workingOn[1] = False
            
    else:
        programError[0] = True
        print("ERROR-3")
        checks[0] = False
        checks[1] = False
        checks[2] = 0
        checks[3] = False
        checks[4] = True
        workingOn[1] = False







# Checks: Var0 - if conditionalBlockStarted | var1 - checkThe functions | var2 - contadorCierraParentesis
def verifyConditionBlockLoopsAndConditionals(currentTocken: str, checks: list, workingOn: list, programError: bool):
    if (checks[0] == False) and (currentTocken == "(") and (workingOn[1] == False):
        workingOn[3] = True
        checks[0] = True
    elif workingOn[3] == True and currentTocken == "(" and workingOn[1] == True:
        pass
    elif workingOn[1] == True:
        pass
    elif (checks[0] == True) and (currentTocken in compFunctions.keys()):
        checks[0] = False
    
    elif (currentTocken == ")"):
        checks[2] += 1
        if checks[2] == 2:
            workingOn[3] = False
            checks[0] = False
            checks[1] = False
            checks[2] = 0 
            
            
    else:
        programError[0] = True
        print(currentTocken)
        print("ERROR-5")




def lexer(txt: str):
    tockens = " ".join(txt).replace(" ", "#").replace("(", "_(_").replace(")", "_)_").replace("{", "_{_").replace("}", "_}_").replace(",", "_,_").replace(";", "_;_")
    tockens = re.split('_|#', tockens)

    while ('' in tockens):
            tockens.remove('')

    return tockens

def programStartEnd(tockens: list):
    try:
        startStatement = tockens.index("PROG")
        endStatement = tockens.index("GORP")
        tockens = tockens[startStatement + 1:endStatement + 1]
        tockenNum = 0
        foundNot = False
        while tockenNum < len(tockens):
            if tockens[tockenNum] == "not":
                tockens.pop(tockenNum)
                tockens.pop(tockenNum)
                foundNot = True
            if foundNot == True and tockens[tockenNum] == ")":
                tockens.pop(tockenNum-1)
                foundNot = False
            tockenNum += 1
            
    except Exception as e: 
        print(e)
        return False
    return tockens




"""
Useful functions
"""

def isNumber(val):
    try:
        float(val)
        return True
    except:
        return False

def getDictVal(valDict: dict, val):
    try:
        return valDict[val]
    except:
        return False

def checkVarType(val: str, val_type: str):
    result = False
    isNumberVal = isNumber(val)
    if isNumberVal == False:
        val = getDictVal(varGlobal, val)
        if val == None:
            return True
        if val == False:
            return False
        
    if isNumberVal == True and val_type == "int_type":
        result = True
    elif isNumberVal == False and val_type == "D_type":
        valid = ["LEFT", "RIGHT", "AROUND"]
        if val in valid:
            result = True
    elif isNumberVal == False and val_type == "d_type":
        valid = ["LEFT", "RIGHT", "FRONT", "BACK"]
        if val in valid:
            result = True
    elif isNumberVal == False and val_type == "o_type":
        valid = ["NORTH", "SOUTH", "WEST", "EAST"]
        if val in valid:
            result = True
            
    # podria daniar
    elif isNumberVal == False and val_type == "functionsGlobal_type":
        valid = functionsGlobal.keys()
        if val in valid:
            result = True
    elif isNumberVal == False and val_type == "compFunction_type":
        valid = compFunctions.keys()
        if val in valid:
            result = True
    
    return result

def validVariableName(varName: str):
    varIsNumber = isNumber(varName)
    if (varIsNumber) or (isNumber(varName[0])) or (len(varName) < 1) or (varName in reservedChars) or (varName in reservedNames) or ("," in varName) or (";" in varName) or ("{" in varName) or ("}" in varName) or ("(" in varName) or (")" in varName) or ("." in varName): # or (varName in varGlobal.keys()) or (varName in functionsGlobal.keys())
        return False
    return True

def isWorking(workingOn: list):
    if workingOn.count(True) > 0:
        return True
    return False

def isWorkingExcept(workingOn: list, num: int):
    if workingOn.count(True) + 1 == len(workingOn) and workingOn[num] == False:
        return True
    return False