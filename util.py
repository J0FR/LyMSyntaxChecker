import re

"""
Reserved characters
"""
reservedChars = [',', ';', '{', '}', '(', ')']
reservedNames = ["if", "else", "fi", "while", "do", "od", "PROG", "GORP", "var", "PROC", "CORP"]


"""
Global Variables
"""

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
    "not": "not"
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
    
    # Last item verifier varChecker
    lastTockenComma = False
    lastTockenVar = False
    
    # Last item verifier existingFunctionsChecker 
    openParenthesesEFC = False
    closeParenthesesEFC = False
    lastTockenCommaEFC = False
    lastTockenVarEFC = False
    
    # Working on processes
    workingOnVar = False
    wokingOnDeclaredFunctions = False
    
    while tockenNum < len(tockens):
        currentTocken = tockens[tockenNum]
        
        # check variable declaration
        if (workingOnVar == True) or (currentTocken == "var"):
            if currentTocken == "var":
                workingOnVar = True
            else:
                if lastTockenComma == True or lastTockenVar == False:
                    valid = validVariableName(currentTocken)
                    lastTockenVar = True
                    lastTockenComma = False
                    if valid == False:
                        error = True
                else:
                    if currentTocken == ";":
                        workingOnVar = False
                        lastTockenVar = False
                        lastTockenComma = False
                    elif currentTocken != ",":
                        error = True
                    lastTockenComma = True
                    lastTockenVar = False
                    
        # check existing functions
        if (wokingOnDeclaredFunctions == True) or (currentTocken in functionsGlobal.keys()):
            if currentTocken in functionsGlobal.keys():
                wokingOnDeclaredFunctions = True
            else:
                if openParenthesesEFC != True and currentTocken != "(":
                    error = True
                else:
                    openParenthesesEFC = True
                    
                pass
        

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
    if (varIsNumber) or (isNumber(varName[0])) or (len(varName) < 1) or (varName in reservedChars) or (varName in reservedNames) or (varName in varGlobal.keys()) or (varName in functionsGlobal.keys()) or ("," in varName) or (";" in varName) or ("{" in varName) or ("}" in varName) or ("(" in varName) or (")" in varName) or ("." in varName):
        return False
    return True