from functools import partial
import re
import enum

class CmpRes(enum.Enum):
    less = 1
    equal = 2
    greater = 3

def generateString(registerDict, x):
    if (x.strip() in registerDict):
        return str(registerDict[x.strip()])
    else:
        return x

def execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    global breakFunc, continueFunc, result, Error
    breakFunc, continueFunc, Error = False, False, False
    result = ""
    indexCommand = 0
    for ex in executionDict[labelName]:

        params = list(ex.values())
        params = params[0][0]
        exFunc = list(ex.keys())[0]

        if(breakFunc):
            break

        if(labelName in returnAddressStack and continueFunc == True):
            if(exFunc == list(returnAddressStack[labelName].keys())[0] and params == returnAddressStack[labelName][exFunc][0]):
                continueFunc = False
                del returnAddressStack[labelName]
        elif(labelName == 0):
            continueFunc = False

        if(continueFunc):
            continue

        if (exFunc == call
                or exFunc == jmp
                or exFunc == jne
                or exFunc == je
                or exFunc == jl
                or exFunc == jle
                or exFunc == jg
                or exFunc == jge
        ):
            exFunc(registerDict, executionDict, params['name'], lastCmpRes, returnAddressStack)
            if(exFunc == call
                    and (indexCommand + 1) < len(executionDict[labelName])):
                returnAddressStack[labelName] = executionDict[labelName][indexCommand + 1]
        elif (exFunc == msg):
            result = result + exFunc(registerDict, executionDict, params['value'])
        elif (exFunc == ret):
            exFunc()
            continueFunc = True
        elif (exFunc == end):
            exFunc()
            breakFunc = True
        else:
            if (exFunc == cmp):
                lastCmpRes = exFunc(registerDict, params['name'], params['value'], lastCmpRes)
            else:
                exFunc(registerDict, params['name'], params['value'])
        indexCommand += 1

        if(labelName != 0 and indexCommand == len(executionDict[labelName])):
            if(exFunc != ret):
                Error = True

    return result

def mov(registerDict, registerName, value):
    if(value in registerDict):
        registerDict[registerName] = registerDict[value]
    else:
        registerDict[registerName] = int(value)
def inc(registerDict, registerName, value):
    registerDict[registerName] = registerDict[registerName] + 1
def dec(registerDict, registerName, value):
    registerDict[registerName] = registerDict[registerName] - 1
def add(registerDict, registerName, value):
    if(not value.isdigit()):
        value = registerDict[value]
    registerDict[registerName] = registerDict[registerName] + int(value)
    registerDict[registerName] = int(registerDict[registerName])
def sub(registerDict, registerName, value):
    if(not value.isdigit()):
        value = registerDict[value]
    registerDict[registerName] = registerDict[registerName] - int(value)
    registerDict[registerName] = int(registerDict[registerName])
def mul(registerDict, registerName, value):
    if(not value.isdigit()):
        value = registerDict[value]
    registerDict[registerName] = registerDict[registerName] * int(value)
    registerDict[registerName] = int(registerDict[registerName])
def div(registerDict, registerName, value):
    if(not value.isdigit()):
        value = registerDict[value]
    registerDict[registerName] = registerDict[registerName] / int(value)
    registerDict[registerName] = int(registerDict[registerName])
def jmp(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)

def cmp(registerDict, value1, value2, lastCmpRes):
    if (value1 in registerDict):
        value1 = registerDict[value1]
    else:
        value1 = int(value1)
    if (value2 in registerDict):
        value2 = registerDict[value2]
    else:
        value2 = int(value2)
    if (value1 < value2):
        lastCmpRes = CmpRes.less
    elif(value1 == value2):
        lastCmpRes = CmpRes.equal
    elif(value1 > value2):
        lastCmpRes = CmpRes.greater
    return lastCmpRes
def jne(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    if (lastCmpRes != CmpRes.equal):
        execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def je(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    if (lastCmpRes == CmpRes.equal):
        execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def jge(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    if (lastCmpRes == CmpRes.greater or lastCmpRes == CmpRes.equal):
        execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def jg(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    if (lastCmpRes == CmpRes.greater):
        execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def jle(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    if (lastCmpRes == CmpRes.less or lastCmpRes == CmpRes.equal):
        execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def jl(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    if(lastCmpRes == CmpRes.less):
        execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def call(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack):
    execution(registerDict, executionDict, labelName, lastCmpRes, returnAddressStack)
def ret():
    pass
def msg(registerDict, executionDict, values):
    partialFunc = partial(generateString, registerDict)
    string = "".join(map(partialFunc, values))
    print(string)
    return string
def end():
    pass


def assembler_interpreter(program):
    executionDict = {0: []}
    instruction = {'mov': mov,
               'inc': inc,
               'dec': dec,
               'add': add,
               'sub': sub,
               'mul': mul,
               'div': div,
               'jmp': jmp,
               'cmp': cmp,
               'jne': jne,
               'je': je,
               'jge': jge,
               'jg': jg,
               'jle': jle,
               'jl': jl,
               'call': call,
               'ret': ret,
               'msg': msg,
               'end': end
               }
    str = ""
    flagComment = False
    flagEnd = False
    functionName = ""
    for c in program:
        if(c == ';'):
            flagComment = True
        if(not flagComment):
            str += c
        if(c == "\n"):
            params = {'name': None, 'value': None}
            flagComment = False
            command = str.strip().replace('\n', "").split(' ')[0]
            if(command == 'mov' or command == 'add' or command == 'sub' or command == 'mul' or command == 'div' or command == 'cmp'):
                params['name'] = str.strip().replace('\n', "").split(',')[0].replace('mov', '').replace('add', '')\
                    .replace('sub', '').replace('mul', '').replace('div', '').replace('cmp', '').strip()
                params['value'] = str.strip().split(',')[1].strip()
            elif(command == 'inc' or command == 'dec' or command == 'call' or command == 'jmp'
                 or command == 'jne'
                 or command == 'je'
                 or command == 'jl'
                 or command == 'jle'
                 or command == 'jg'
                 or command == 'jge'
            ):
                params['name'] = str.strip().replace('\n', "").replace('inc', "").replace('dec', "")\
                    .replace('call', "").replace('jmp', "")\
                    .replace('jne', "").replace('jle', "").replace('jge', "").replace('jl', "").replace('jg', "").replace('je', "").strip()
                params['value'] = ''
            elif(command == 'end'):
                flagEnd = True
            elif(command.find(':') != -1):
                functionName = str.strip().replace('\n', "").split(':')[0]
                executionDict[functionName] = []
            elif (command == 'msg'):
                str = str.replace("msg", "").strip()
                params['value'] = re.findall("\'(.*?)\'|([^',\s]*)", str)
                params['value'] = list(filter(lambda x : x.strip(' '), [(''.join(x)) for x in params['value']]))
            if(command != '' and command.find(':') == -1):
                if(functionName != ''):
                    executionDict[functionName].append({instruction[command]: [params]})
                    if(command == 'ret'):
                        functionName = ''
                else:
                    executionDict[0].append({instruction[command]: [params]})
            str = ""

    registerDict = {}
    lastCmpRes = 0
    returnAddressStack = {}
    result = execution(registerDict, executionDict, 0, lastCmpRes, returnAddressStack)

    if(flagEnd and registerDict != {} and not Error):
        return result

    return -1

program = """
mov   a, 11           ; value1
mov   b, 3            ; value2
call  mod_func
msg   'mod(', a, ', ', b, ') = ', d        ; output
end

; Mod function
mod_func:
    mov   c, a        ; temp1
    div   c, b
    mul   c, b
    mov   d, a        ; temp2
    sub   d, c
    ret
"""

print(assembler_interpreter(program))