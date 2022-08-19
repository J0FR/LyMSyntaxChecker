from audioop import reverse


def lexer(lista: list):
    
    lista_final = []
    
    while ('' in lista):
        lista.remove('')
    
    counter = 0
    for line in lista:
        # remove extra spaces and tabulations
        lista[counter] = line.strip()
        
        stringStart = 0
        counter2 = 0
        was = False
        for caracter in line:
            
            if caracter == "," or caracter == ";" or caracter == "{" or caracter == "}" or caracter == ")" or caracter == "(":
                
                # print(f"start: {stringStart}")
                # print(f"contador: {counter2}")
                # print(len(line))
                lista_final.append(line[stringStart:counter2])
                
                # if caracter == ";":
                #     print("el propio")
                #     print(f"startasdf: {stringStart}")
                #     print(f"contadoadsfr: {counter2}")
                if was == True:
                    # print(lista_final)
                    # print(len(lista_final))
                    value = lista_final.pop(len(lista_final) - 1)
                    lista_final.append(value[0:1])
                    lista_final.append(value[1:])
                    # print(f"startasdf: {stringStart}")
                    # print(f"contadoadsfr: {counter2}")
                    was = False
                    
                if caracter == "(":
                    was = True
                
                #esto se puede unir con el siguiente condicional
                if counter2 == len(line) - 1:
                    lista_final.append(line[counter2:len(line)])
                stringStart = counter2 
                
                    
                
            elif caracter == " ":
                lista_final.append(line[stringStart:counter2])
                # print(f"start: {stringStart}")
                # print(f"contador: {counter2}")
                stringStart = counter2 +1
                counter2 += 1
                continue
            if ("while" in line) and ("do" in line) and len(lista_final) != 0 and (lista_final[-1] == "}"):
                    lista_final.append("od")
            if ("if" in line) and len(lista_final) != 0 and (lista_final[-1] == "}"):
                    lista_final.append("fi")
                

                
            
            counter2 += 1
                
        counter += 1
        
    
    while ('' in lista_final):
        lista_final.remove('') 
        
    print(lista_final)


filename = 'files/test2.txt'

with open(filename) as f:
    lines = f.read().splitlines()
    
startStatement = lines.index("PROG")
endStatement = lines.index("GORP")

lines = lines[startStatement + 1:endStatement]

lexer(lines)

for elementNum in range(startStatement + 1, endStatement):
    #print(elementNum)
    pass

