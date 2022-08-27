import re

"""
Reserved characters
"""
reservedChars = [',', ';', '{', '}', '(', ')', '=']
checkersForProgramCheck = ["if", "per", "else", "fi", "while", "do", "od", "PROG", "GORP", "var", "PROC", "CORP", "repeatTimes", "GORP",
                           '{', '}']
closeChars = ["CORP", ";"]
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
funcVacios = []

localVar = []

varGlobal = ["[default]"]

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
        "go": [1, 2],
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
workingOnInstructionBlockFunctionCreation = [False, False, False, False, False, False, False]


            # Working on function creation
workingOnFunctionCreation = [False, False, False, False, False, False, False, False, False]


"""
Main Functions
"""
def runProgram(tockens: list):
    tockenNum = 0
    
    usingFunction = None
    started = True
    print(tockens)
    
    while tockenNum < len(tockens):
        currentTocken = tockens[tockenNum]
        if programError[0] == False and (currentTocken in reservedChars or currentTocken in reservedNames or currentTocken in varGlobal or currentTocken in functionsGlobal.keys() or isNumber(currentTocken) or currentTocken == "[default]"): 
            if workingOn[1] == True or currentTocken in functionsGlobal.keys():
                if workingOnExistingFunctionsChecks[4] == True:
                    usingFunction = functionsGlobal[currentTocken]
                    workingOnExistingFunctionsChecks[4] = False
                verifyExistingFunctions(currentTocken, workingOnExistingFunctionsChecks, workingOn, programError, usingFunction)
            if currentTocken in varGlobal and (tockens[tockenNum - 1] != ";" and tockens[tockenNum - 1] != "{" and workingOn[1] == False):
                programError[0] = True
                print("ERROR-32")
            elif currentTocken in functionsGlobal.keys() and (tockens[tockenNum - 1] != ";" and tockens[tockenNum - 1] != "{"):
                programError[0] = True
                print("ERROR-33")
                # print(tockens[tockenNum - 1])
            elif currentTocken == ";" or currentTocken == "}":
                if tockens[tockenNum - 1] != ")" and isNumber(tockens[tockenNum - 1]) == False:
                    programError[0] = True
                    print("ERROR-34")
            if currentTocken == "}":
                pass
        else:
            programError[0] = True
            break
        tockenNum += 1
    if programError[0] == True:
        return True
    else:
        return False
            
def parser(tockens: list):
            # Important parser Variables
    tockenNum = 0
    closeParenthesesChecker = False
    
    # print(tockens)
    while tockenNum < len(tockens):
        currentTocken = tockens[tockenNum]
        if programError[0] == False and (currentTocken in reservedNames or currentTocken in reservedChars or (isWorking(workingOn) and validVariableName(currentTocken)) or (isWorking(workingOn) and isNumber(currentTocken))):
            if currentTocken == "not" and tockens[tockenNum + 1] == "(":
                # print("llegueeee")
                closeParenthesesChecker = True
                tockenNum += 2
                # print(tockens[tockenNum])
            if closeParenthesesChecker == True and currentTocken == ")":
                closeParenthesesChecker = False
                tockenNum += 1
            if workingOn[0] == True or currentTocken == "var":
                verifyVariableDeclaraction(currentTocken, workingOnVariableChecks, workingOn, programError)
            if (workingOn[1] == True or currentTocken in functionsGlobal.keys()):
                if workingOnExistingFunctionsChecks[4] == True:
                    usingFunction = functionsGlobal[currentTocken]
                    workingOnExistingFunctionsChecks[4] = False
                verifyExistingFunctions(currentTocken, workingOnExistingFunctionsChecks, workingOn, programError, usingFunction)
            if workingOn[7] or currentTocken == "PROC":
            # instructionBlockFunctionCreation(currentTocken, workingOnInstructionBlockFunctionCreation, workingOn, programError)
                FunctionCreation(currentTocken, workingOnFunctionCreation, workingOn, programError)
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
        checks[8] = True
    elif checks[4] == True and (validVariableName(currentTocken)) and workingOn[6] == False:
        #VARIABLES LOCALES
        localVar.append(currentTocken)
        varGlobal.append(currentTocken)
        reservedNames.append(currentTocken)
        num = checks[2][0] + 1
        checks[2].pop(0)
        checks[2].append(num)
        checks[4] = False
        checks[7] = True
    elif checks[4] == False and currentTocken == "," and checks[7] == True:
        checks[4] = True
        checks[7] = False
    elif checks[5] == True:
        
        instructionBlockFunctionCreation(currentTocken, workingOnInstructionBlockFunctionCreation, workingOn, programError)
        if workingOn[6] == False:
            checks[5] = False
            checks[6] = True
    elif checks[4] == False and currentTocken == ")":
        checks[5] = True
    elif currentTocken == "CORP":
        for i in localVar:
            varGlobal.remove(i)
            reservedNames.remove(i)
        localVar.clear()
        workingOn[7] = False
        checks[0] = False
        checks[1] = False
        checks[2] = [0]
        checks[3] = False
        checks[4] = False
        checks[5] = False
        checks[6] = False
        checks[7] = False
    
    else:
        programError[0] = True
        print("ERROR-9")

# InstructionBlockFunctionCreation
# checks: var0: check { character | var1: checks the current instruction structure | var2: checks that existingFunctionsChecking is done
# var3: woking on conditional declaration | var 4: working on loops declaration
def instructionBlockFunctionCreation(currentTocken: str, checks: list, workingOn: list, programError: bool):
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
        checks[6] = False
    elif workingOn[6] == False or currentTocken == "CORP":
        pass
    else:
        programError[0] = True
        print("ERROR-10")
        
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
    elif workingOn[2] or (checks[3] and currentTocken == "else"):
        checks[4] = True
    elif workingOn[2] or (checks[4] and currentTocken == "{"):
        checks[4] = False
        verifyInstructionBlockLoopsAndConditionals(currentTocken, workingOnBodyConditionalsChecks, workingOn, programError)
        if workingOn[2] == False:
            checks[5] = True
    elif currentTocken == "fi":
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
    #print(workingOn[3])
    if currentTocken == "while" and checks[0] == False:
        workingOn[4] = True
        checks[0] = True
        checks[1] = True
    elif workingOn[3] or (checks[1] == True and currentTocken == "("):
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
        print(f"check2 {checks[2]}")
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
        print(currentTocken)
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
        print("ERROR-5")
        print(currentTocken)

def lexer(txt: str):
    tockens = " ".join(txt).replace(" ", "#").replace("(", "_(_").replace(")", "_)_").replace("{", "_{_").replace("}", "_}_").replace(",", "_,_").replace(";", "_;_").replace("=", "_=_")
    tockens = re.split('_|#', tockens)
    while ('' in tockens):
            tockens.remove('')
    return tockens

def programStartEnd(tockens: list):
    try:
        tockenNum = 0
        foundNot = False
        lastBadChar = -1
        while tockenNum < len(tockens):
            if tockens[tockenNum] == "not":
                tockens.pop(tockenNum)
                tockens.pop(tockenNum)
                foundNot = True
            if foundNot == True and tockens[tockenNum] == ")":
                tockens.pop(tockenNum-1)
                foundNot = False
            if tockens[tockenNum] == "{":
                lastBadChar = tockenNum
            tockenNum += 1
        if tockens[lastBadChar - 1] not in closeChars or tockens[len(tockens)-1] != "GORP":
            return False, False
        tockensProgramRun = tockens[lastBadChar:-1]
        tockens = tockens[0:lastBadChar]
        tockens.append("GORP")
        startStatement = tockens.index("PROG")
        endStatement = tockens.index("GORP")
        tockenNum = 0
        while tockenNum < len(tockens):
            if tockens[tockenNum] == "PROC" and validVariableName(tockens[tockenNum + 1]) and tockens[tockenNum + 2] == "(" and tockens[tockenNum + 3] == ")":
                tockens.insert(tockenNum + 3, "[default]")
                funcVacios.append(tockens[tockenNum + 1])
                tockenNum += 1
            tockenNum += 1
        tockenNum = 0
        while tockenNum < len(tockensProgramRun):
            if tockensProgramRun[tockenNum] in funcVacios and tockensProgramRun[tockenNum + 1] == "(" and tockensProgramRun[tockenNum + 2] == ")":
                tockensProgramRun.insert(tockenNum + 2, "[default]")
                tockenNum += 1
            tockenNum += 1
        tockens = tockens[startStatement + 1:endStatement ]
    except Exception as e: 
        print(tockens[tockenNum])
        print(e)
        return False, False
    return tockens, tockensProgramRun

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

def validVariableName(varName: str):
    varIsNumber = isNumber(varName)
    if (varIsNumber) or (isNumber(varName[0])) or (len(varName) < 1) or (varName in reservedChars) or (varName in reservedNames) or ("," in varName) or (";" in varName) or ("{" in varName) or ("}" in varName) or ("(" in varName) or (")" in varName) or ("." in varName): # or (varName in varGlobal.keys()) or (varName in functionsGlobal.keys())
        return False
    return True

def isWorking(workingOn: list):
    if workingOn.count(True) > 0:
        return True
    return False