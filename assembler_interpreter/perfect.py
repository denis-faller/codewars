from operator import add, sub, mul, floordiv as div, lt, le, eq, ne, ge, gt
import re

TOKENIZER = re.compile(r"('.*?'|-?\w+)[:,]?\s*")
SKIP_COMMENTS = re.compile("\s*;")
SPLIT_PROG = re.compile(r'\n\s*')

CMP_FUNCS = {'jmp': lambda x, y: True, 'jne': ne, 'je': eq, 'jge': ge, 'jg': gt, 'jle': le, 'jl': lt}
MATH_FUNCS = {'add', 'sub', 'mul', 'div', 'inc', 'dec'}
MATH_DCT = {'inc': 'add', 'dec': 'sub'}

JUMPS_CMD = set(CMP_FUNCS.keys()) | {'call'}
ALL_CMDS = {'ret', 'end', 'mov', 'cmp', 'msg'} | JUMPS_CMD


def assembler_interpreter(program):
    def tokenize(s):
        return TOKENIZER.findall(SKIP_COMMENTS.split(s)[0])

    def updateCmp(x, y):
        return {k: op(reg.get(x, 0), reg[y] if y.isalpha() else int(y)) for k, op in CMP_FUNCS.items()}

    def moveTo(cmdJump, lbl):
        return jumps_lbl[lbl] if cmpDct[cmdJump] else p

    def updateReg(op, x, y='1', val=None):
        reg[x] = op(reg[x] if val is None else val, reg[y] if y.isalpha() else int(y))

    p, reg, output, callStackP = 0, {}, '', []
    inst = [cmd for cmd in map(tokenize, SPLIT_PROG.split(program)) if cmd]
    jumps_lbl = {cmd[0]: i for i, cmd in enumerate(inst) if cmd[0] not in ALL_CMDS}
    cmpDct = updateCmp('0', '0')

    while 0 <= p < len(inst):
        cmd, xyl = inst[p][0], inst[p][1:]

        if cmd == 'mov':
            updateReg(add, xyl[0], xyl[1], 0)
        elif cmd == 'cmp':
            cmpDct = updateCmp(xyl[0], xyl[1])
        elif cmd in MATH_FUNCS:
            updateReg(eval(MATH_DCT.get(cmd, cmd)), *xyl)
        elif cmd in CMP_FUNCS:
            p = moveTo(cmd, xyl[0])
        elif cmd == 'call':
            callStackP.append(p); p = moveTo('jmp', xyl[0])
        elif cmd == 'ret':
            p = callStackP.pop()
        elif cmd == 'end':
            return output
        elif cmd == 'msg':
            output += ''.join(s[1:-1] if s not in reg else str(reg[s]) for s in inst[p][1:]); print(output)
        p += 1

    return -1


program = """
mov   a, 5
mov   b, a
mov   c, a
call  proc_fact
call  print
end

proc_fact:
    dec   b
    mul   c, b
    cmp   b, 1
    jne   proc_fact
    ret

print:
    msg   a, '! = ', c ; output text
    ret
"""

print(assembler_interpreter(program))