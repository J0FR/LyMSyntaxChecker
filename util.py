import re

"""
Reserved characters
"""
reservedChars = [',', ';', '{', '}', '(', ')', '=']
reservedNames = ["if", "else", "fi", "while", "do", "od", "PROG", "GORP", "var", "PROC", "CORP"]


"""
Global Variables
"""

localVar = []

varGlobal = {
    "north": "NORTH",
    "south": "SOUTH",
    "east": "EAST",
    "west": "WEST",
    
    "front": "FRONT",
    "right": "RIGHT",
    "left": "LEFT",
    "back": "BACK",
    
    "around": "AROUND",
    
    #functionsGlobal
    "walk": "walk",
    "jump": "jump",
    "jumpTo": "jumpTo",
    "veer": "veer",
    "look": "look",
    "drop": "drop",
    "grab": "grab",
    "get": "get",
    "free": "free",
    "pop": "pop",
    
        
    # compFunctions
    "isfacing": "isfacing",
    "isValid": "isValid",
    "canWalk": "canWalk",
    "not": "not",
    
    }  

functionsGlobal = {
        "walk": [["int_type"], ["d_type", "int_type"], ["o_type", "int_type"]],
        "jump": [["int_type"]],
        "jumpTo": [["int_type", "int_type"]],
        "veer": [["D_type"]],
        "look": [["o_type"]],
        "drop": [["int_type"]],
        "grab": [["int_type"]],
        "get": [["int_type"]],
        "free": [["int_type"]],
        "pop": [["int_type"]],
        "go": [["int_type"]],
        
        #compFunctions
        "isfacing": [["o_type"]],
        "isValid": [["functionsGlobal_type", "int_type"]],
        "canWalk": [["o_type", "int_type"], ["d_type", "int_type"]],
        "not": ["compFunction_type"]
    }

compFunctions = {
    "isfacing": [["o_type"]],
    "isValid": [["functionsGlobal_type", "int_type"]],
    "canWalk": [["o_type", "int_type"], ["d_type", "int_type"]],
    "not": ["compFunction_type"]
}



"""
Main Functions
"""

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
        tockens = tockens[startStatement + 1:endStatement]
    except:
        return False
    return tockens

def parser(tockens: list):
    tockenNum = 0
    error = False
    
    # Running program
    theProgramIsRunning = True
    
    # Last item verifier varChecker
    lastTockenComma = False
    lastTockenVar = False
    
    # Last item verifier existingFunctionsChecker 
    openParenthesesEFC = False
    lastTockenCommaEFC = False
    lastTockenVarEFC = False
    parameterNumber = 0
    parameterTypeMatch = []
    usingFunction = None
    
    # Last item verifier creatingFunctionsChecker 
    openParametersCFC = False
    workingOnParametersCFC = False
    lastTockenCommaCFC = False
    lastTockenVarCFC = False
    openCurlyBracketCFC = False
    nameFunctionCFC = ""
    workingOnBodyCFC = False
    nextClose = False
    
    # verifier for conditionalsSyntaxChecker
    openConditionalCSC = False
    openInstructionsCSC = False
    buildingConditionalCSC = False
    buildingInstructionsCSC = False
    closedParenthesesCSC = False
    conditionalCheck = False
    instructionCheckCSC = False
    closedCurlyBracketsCSC = False


    # Working on processes
    workingOnVar = False
    wokingOnDeclaredFunctions = False
    workingOnNewFunction = False
    
    workingOnConditional = False
    workingOnLoops = False
    workingOnCompFunctions = False
    workingOnFunctionsGlobal = False  
    workingOnLoop = False  
    
    # Item verifier loops
    
    openConditionalLoop = False
    buildingConditionalLoop = False
    conditionalCheckLoop = False
    closedParenthesesLoop = False   
    openInstructionsLoop = False     
    buildingInstructionsLoop = False 
    instructionCheckLoops = False      
    closedCurlyBracketsLoop = False      

    while tockenNum < len(tockens):
        currentTocken = tockens[tockenNum]
        lastTockenRepetition = tockens[tockenNum-1]
        secondToLastRepetition = tockens[tockenNum-2]
        if currentTocken in reservedNames or currentTocken in varGlobal or isNumber(currentTocken) or (currentTocken in reservedChars) or workingOnVar or workingOnParametersCFC or workingOnConditional or workingOnLoops:
            
            
            
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                            
                            
                            
                            
                            
                            
                            
                            
                            
                    
            if (workingOnVar == True) or (currentTocken == "var"):
                if currentTocken == "var":
                    workingOnVar = True
                else:
                    if lastTockenComma == True or lastTockenVar == False:
                        valid = validVariableName(currentTocken)
                        varGlobal[currentTocken] = None
                        lastTockenVar = True
                        lastTockenComma = False
                        if valid == False:
                            error = True
                            print("12")
                    else:
                        if currentTocken == ";":
                            workingOnVar = False
                            lastTockenVar = False
                            lastTockenComma = False
                        elif currentTocken != ",":
                            error = True
                            print("13")
                            
                        lastTockenComma = True
                        lastTockenVar = False
            
                
                
            # check existing functions
            
            if (wokingOnDeclaredFunctions == True) or (currentTocken in functionsGlobal.keys()) and workingOnLoop != True:
                if currentTocken in functionsGlobal.keys():
                    wokingOnDeclaredFunctions = True
                    usingFunction = functionsGlobal[currentTocken]
                    parameterTypeMatch = [0]*len(usingFunction)
                    
                    nextTocken = tockens[tockenNum + 1]
                    worksVoid = 0
                    for i in usingFunction: 
                        if len(i) == 0:
                            worksVoid += 1
                        else:
                            worksVoid += 0
                    if nextTocken != ")" and worksVoid > 0:
                        wokingOnDeclaredFunctions = False
                    
                else:
                    if openParenthesesEFC == True:
                        if lastTockenCommaEFC == True or lastTockenVarEFC == False:
                            i = 0
                            for function in usingFunction:
                                if parameterNumber < len(function) and checkVarType(currentTocken, function[parameterNumber]):
                                    parameterTypeMatch[i] += 1
                                i += 1
                            parameterNumber += 1
                            lastTockenCommaEFC = False
                            lastTockenVarEFC = True      
                        else:
                            if currentTocken == ")":
                                working = 0
                                pivot = 0
                                while pivot < len(usingFunction):
                                    if len(usingFunction[pivot]) <= parameterTypeMatch[pivot]:
                                        working += 1
                                    pivot += 1
                                if working == 0:
                                    error = True  
                                    print("14")
                                wokingOnDeclaredFunctions = False
                                openParenthesesEFC = False
                                lastTockenVarEFC = False
                                parameterNumber = 0
                                parameterTypeMatch = []
                                usingFunction = None
                            elif currentTocken != ",":
                                error = True
                                
                                print("15")
                            lastTockenCommaEFC = True
                            lastTockenVarEFC = False
                    else:
                        previousTocken = tockens[tockenNum - 1]
                        if currentTocken != "(":
                            error = True
                            print("16")
                        if previousTocken not in functionsGlobal.keys():
                            error = True
                            print("17")
                        openParenthesesEFC = True
            

            #Checks the creation of functions
            
            if ((workingOnNewFunction == True) or (currentTocken == "PROC")) and workingOnLoop == False:
                if currentTocken == "PROC":
                    varGlobal[tockens[tockenNum + 1]] = tockens[tockenNum + 1]
                    functionsGlobal[tockens[tockenNum + 1]] = []
                    functionsGlobal[tockens[tockenNum + 1]].append([])
                    nameFunctionCFC = tockens[tockenNum + 1]
                    workingOnNewFunction = True
                    openParametersCFC = True
                    workingOnParametersCFC = True
                    tockenNum += 2
                    continue
                else:
                    
                    if workingOnParametersCFC == True:
                        if workingOnParametersCFC == True and openParametersCFC == True and currentTocken != "(":
                            error = True
                            print("18")
                            
                        elif workingOnParametersCFC == True:
                            if openParametersCFC == True and currentTocken == "(":
                                openParametersCFC = False
                                nextTocken = tockens[tockenNum + 1]
                                if nextTocken != ")":
                                    workingOnParametersCFC = True
                                else:
                                    workingOnParametersCFC = False
                            elif workingOnParametersCFC == True and (lastTockenCommaCFC == True or lastTockenVarCFC == False):
                                # adding variables from the parameters
                                varGlobal[currentTocken] = None
                                functionsGlobal[nameFunctionCFC][-1].append("int_type")
                                localVar.append(currentTocken)
                                
                                lastTockenVarCFC = True
                                lastTockenCommaCFC = False
                            elif workingOnParametersCFC == True and (lastTockenCommaCFC == False or lastTockenVarCFC == True):
                                if currentTocken == ",":
                                    lastTockenVarCFC = False
                                    lastTockenCommaCFC = True
                                elif currentTocken == ")":
                                    lastTockenVarCFC = False
                                    lastTockenCommaCFC = False
                                    
                                    workingOnParametersCFC = False
                                    openCurlyBracketCFC = True
                                    
                                else:
                                    error = True
                                    print("19")
                                    
                    elif openCurlyBracketCFC == True:
                        
                        if workingOnBodyCFC == False and currentTocken != "{":
                            error = True
                            print("20")

                        else:
                            if workingOnBodyCFC == False and currentTocken == "{":
                                workingOnBodyCFC = True
                            else:
                                if currentTocken in ["fi", "od", ")"]:
                                    nextClose = True
                                elif nextClose == True:
                                    if currentTocken == ";":
                                        nextClose = False
                                    elif currentTocken == "}":
                                        nextTocken = tockens[tockenNum + 1]
                                        if nextTocken != "CORP":
                                            error = True
                                            print("21")
                                            
                                        else:
                                            openParametersCFC = False
                                            workingOnParametersCFC = False
                                            lastTockenCommaCFC = False
                                            lastTockenVarCFC = False
                                            openCurlyBracketCFC = False
                                            nameFunctionCFC = ""
                                            workingOnBodyCFC = False
                                            nextClose = False
                                            for i in localVar:
                                                del varGlobal[i]
                                    else:
                                        error = True
                                        print("22")
                if currentTocken == "CORP":
                    workingOnNewFunction = False
            
            # Check conditionals
            if (workingOnConditional == True) or (currentTocken == "if"):
                if currentTocken == "if":
                    workingOnConditional = True
                    openConditionalCSC = True
                    buildingConditionalCSC = True
                else:
                    
                    # build conditionals
                    if buildingConditionalCSC:
                        if openConditionalCSC == True and currentTocken != "(":
                            error = True
                            print("23")
                        elif (openConditionalCSC == False) or (openConditionalCSC == True and currentTocken == "("):
                            if currentTocken == "(":
                                if tockens[tockenNum + 1] == ")":
                                    error = True
                                    print("24")
                                    
                                openConditionalCSC = False
                            elif conditionalCheck == False and tockens[tockenNum - 1] == "(":
                                conditionalCheck = True
                                if currentTocken not in compFunctions.keys():
                                    error = True
                                    print("25")
                                    
                            elif currentTocken == ")":
                                if closedParenthesesCSC == False and currentTocken == ")" and tockens[tockenNum + 1] == ")":
                                    closedParenthesesCSC = True
                                    openInstructionsCSC = True
                                    buildingInstructionsCSC = True
                                    buildingConditionalCSC = False
                                    tockenNum += 2
                                    continue
                                elif closedParenthesesCSC == False:
                                    error = True
                                    print("26")
                                    
                                    
                    # build instructions
                    elif buildingInstructionsCSC:
                        if openInstructionsCSC == True and currentTocken != "{":
                            error = True
                            print("27")
                        elif (openInstructionsCSC == False) or openInstructionsCSC == True and currentTocken == "{":
                            if currentTocken == "{":
                                if tockens[tockenNum + 1] == "}":
                                    error = True
                                    print("28")
                                    
                                openInstructionsCSC = False
                            elif instructionCheckCSC == False and tockens[tockenNum - 1] == "{":
                                instructionCheckCSC = True
                                if currentTocken not in functionsGlobal.keys(): # importante modificar
                                    error = True
                                    print("29")
                                    
                            elif currentTocken == "}":
                                if closedCurlyBracketsCSC == False and currentTocken == "}" and (tockens[tockenNum + 1] == "fi" or tockens[tockenNum + 1] == "else"):
                                    if tockens[tockenNum + 1] == "else":
                                        openConditionalCSC = True
                                        openInstructionsCSC = False
                                        buildingConditionalCSC = True
                                        buildingInstructionsCSC = False
                                        closedParenthesesCSC = False
                                        conditionalCheck = False
                                        instructionCheckCSC = False
                                        closedCurlyBracketsCSC = False
                                        tockenNum += 2
                                        continue
                                    workingOnConditional = False
                                    openConditionalCSC = False
                                    openInstructionsCSC = False
                                    buildingConditionalCSC = False
                                    buildingInstructionsCSC = False
                                    closedParenthesesCSC = False
                                    conditionalCheck = False
                                    instructionCheckCSC = False
                                    closedCurlyBracketsCSC = False
                                    
                                elif closedCurlyBracketsCSC == False:
                                    error = True
                                    print("30")


            # Check conditionals
            if (workingOnLoop == True) or (currentTocken == "while"):
                if currentTocken == "while":
                    workingOnLoop = True
                    openConditionalLoop = True
                    buildingConditionalLoop = True
                else:
                    
                    # build conditionals
                    if buildingConditionalLoop:
                        if openConditionalLoop == True and currentTocken != "(":
                            error = True
                            print("23")
                        elif (openConditionalLoop == False) or (openConditionalLoop == True and currentTocken == "("):
                            if currentTocken == "(":
                                if tockens[tockenNum + 1] == ")":
                                    error = True
                                    print("24")
                                    
                                openConditionalLoop = False
                            elif conditionalCheckLoop == False and tockens[tockenNum - 1] == "(":
                                conditionalCheckLoop = True
                                if currentTocken not in compFunctions.keys():
                                    error = True
                                    print("25")
                                    
                            elif currentTocken == ")":
                                if closedParenthesesLoop == False and currentTocken == ")" and tockens[tockenNum + 1] == ")" and tockens[tockenNum + 2] == "do":
                                    closedParenthesesLoop = True
                                    openInstructionsLoop = True
                                    buildingInstructionsLoop = True
                                    buildingConditionalLoop = False
                                    tockenNum += 3
                                    continue
                                elif closedParenthesesLoop == False:
                                    error = True
                                    print("26")
               
                                    
                    # build instructions
                    elif buildingInstructionsLoop:
                        if openInstructionsLoop == True and currentTocken != "{":
                            error = True
                            print("27")
                        elif (openInstructionsLoop == False) or openInstructionsLoop == True and currentTocken == "{":
                            if currentTocken == "{":
                                if tockens[tockenNum + 1] == "}":
                                    error = True
                                    print("28")
                                    
                                openInstructionsLoop = False
                            elif instructionCheckLoops == False and tockens[tockenNum - 1] == "{":
                                instructionCheckLoops = True
                                if currentTocken not in functionsGlobal.keys(): # importante modificar
                                    error = True
                                    
                                    print("29")
                                    
                            elif currentTocken == "}":
                                if closedCurlyBracketsLoop == False and currentTocken == "}" and (tockens[tockenNum + 1] == "od"):
                                    workingOnLoop = False
                                    openConditionalLoop = False
                                    openInstructionsLoop = False
                                    buildingConditionalLoop = False
                                    buildingInstructionsLoop = False
                                    closedParenthesesLoop = False
                                    conditionalCheckLoop = False
                                    instructionCheckLoops = False
                                    closedCurlyBracketsLoop = False
                                    
                                elif closedCurlyBracketsLoop == False:
                                    error = True
                                    
                                    print("30")

            # Check if program started running
            if theProgramIsRunning == False:    
                if currentTocken == "=" and tockens[tockenNum - 1] not in varGlobal:
                    error = True
                    print("31")
                if currentTocken in varGlobal and varGlobal[currentTocken] == None and tockens[tockenNum + 1] == "=":
                    if isNumber(tockens[tockenNum + 2]) == False:
                        error = True
                        print("32")
                    varGlobal[currentTocken] = tockens[tockenNum + 2]
                    if tockens[tockenNum + 3] != ";" and tockens[tockenNum + 3] != "}":
                        error = True
                        print("33")
                    tockenNum += 3
                    continue
                elif currentTocken in varGlobal and varGlobal[currentTocken] == None and tockens[tockenNum + 1] != "=":
                    error = True
                    print("34")
                if currentTocken in ["fi", "od", ")"]:
                    nextClose = True
                elif nextClose == True:
                    if currentTocken == ";":
                        nextClose = False
                    elif currentTocken == "}":
                        pass
                    else:
                        error = True
                        print("35")
            
            if currentTocken == "{" and (workingOnVar == False and wokingOnDeclaredFunctions == False and workingOnNewFunction == False and workingOnConditional == False):
                    theProgramIsRunning = False      
        else:
            error = True
            print("36")
        if error == True:
            break    
        tockenNum += 1
    return error

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