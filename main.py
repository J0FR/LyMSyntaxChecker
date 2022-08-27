import re
import util as u

def main(filename):
    with open(f"files/{filename}.txt") as temp_file:
        txt = [line.strip() for line in temp_file]

    # Converts txt file str into a list with the tockens that made up the program
    tockens = u.lexer(txt)
    # Checks for PROG and GORP and limit the instructions
    tockens, tockensProgramRun = u.programStartEnd(tockens)
    if tockens == False or tockensProgramRun == False: 
        return True
    
    if u.parser(tockens) == True or u.runProgram(tockensProgramRun) == True:
        return True
    return False
    
def runProgram():
    print("Type the file name located in the folder files that you want to run (without .txt). If you leave it in blanc it's going to run by default main_prueba.txt")
    filename = input("- ")
    if filename == "":
        filename = 'main_prueba'
    result = main(filename)
    if result == False:
        print(f"The program syntax is correct :)")
    else:
        print(f"The program syntax is incorrect :(")

runProgram()
