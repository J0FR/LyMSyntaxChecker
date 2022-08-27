a = [True, True, False]



def isWorkingExcept(workingOn: list, num: int):
    if workingOn.count(True) + 1 == len(workingOn) and workingOn[num] == False:
        return True
    return False

print(len(a))
print(a.count(True))
print(isWorkingExcept(a, 2))