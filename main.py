import re
import util as u

def main(filename):
    with open(f"files/{filename}.txt") as temp_file:
        txt = [line.strip() for line in temp_file]

    # Converts txt file str into a list with the tockens that made up the program
    tockens = u.lexer(txt)
    # Checks for PROG and GORP and limit the instructions
    tockens, tockensProgramRun = u.programStartEnd(tockens)
    # print(tockensProgramRun)
    # print()
    # print(tockens)
    if tockens == False or tockensProgramRun == False: # 
        return True
    
    
    if u.parser(tockens) == True or u.runProgram(tockensProgramRun) == True:
        return True
    return False
    

filename = 'main_prueba'
result = main(filename)
if result == False:
    print(f"El programa esta bien :)")
else:
    print(f"El programa esta mal :(")

