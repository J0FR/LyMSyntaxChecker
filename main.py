import re
import util as u

def main(filename):
    with open(f"files/{filename}.txt") as temp_file:
        txt = [line.strip() for line in temp_file]

    # Converts txt file str into a list with the tockens that made up the program
    tockens = u.lexer(txt)
    # Checks for PROG and GORP and limit the instructions
    tockens = u.programStartEnd(tockens)
    if tockens == False:
        return False
        
    return u.parser(tockens)
    
    # print(tockens)

filename = 'test2'
result = main(filename)
print(result)

