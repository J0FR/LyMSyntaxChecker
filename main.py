import re
import util as u

def main(filename):
    with open(f"files/{filename}.txt") as temp_file:
        txt = [line.strip() for line in temp_file]

    # Converts txt file str into a list with the tockens that made up the program
    tockens = u.lexer(txt)
    # Checks for PROG and GORP and limit the instructions
    tockens = u.programStartEnd(tockens)
    print(tockens)
    if tockens == False:
        return True
    
    
        
    return u.parser(tockens)
    

filename = 'test2'
result = main(filename)
if result == False:
    print(f"El programa esta bien :)")
else:
    print(f"El programa esta mal :(")

